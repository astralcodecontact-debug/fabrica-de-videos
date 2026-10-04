#!/usr/bin/env python3
"""Sobe e agenda os videos de musica no YouTube pela API oficial, sem intervencao.

Comandos:
  autorizar --canal <slug>        abre o navegador uma vez; escolha o canal certo na tela do Google
  enviar <pasta do canal> --canal <slug> [--simular]
  enviar-todos [--simular]        percorre todos os canais de musica de canais/canais.json
  status                          mostra canais autorizados e o que ja foi enviado

Para cada Videos finais/<nome>_video<N>.mp4 com <nome>_video<N>_info.json ao lado e que ainda
nao esta em enviados.json, o script:
  1. passa pela trava (resolucao, duracao, audio, textos); se reprovar, nao sobe e registra o motivo;
  2. sobe (envio retomavel), agenda para publicar_em (se a data ja passou, publica na hora);
  3. coloca a thumbnail (Artes/<N>_thumb.* ou Artes/<N>.*, convertida para JPG 1280x720 < 2 MB);
  4. adiciona na playlist se info.json tiver playlist_id;
  5. grava o resultado em enviados.json e em ~/.capitao/youtube/registro.log.
Se a cota diaria da API acabar, para e sai com codigo 3; a proxima execucao continua de onde parou.

info.json:
  {"titulo": "...", "descricao": "...", "tags": ["..."], "publicar_em": "2026-10-05T18:00:00-04:00",
   "playlist_id": "PL... (opcional)", "categoria": "10 (opcional, 10 = Musica)"}

Caminhos do Mac (raiz_canais_mac) vem de ~/.capitao/local.json, que sobrescreve canais.json.
Credenciais ficam FORA do repositorio, em ~/.capitao/youtube/:
  client_secret.json   (baixado do Google Cloud, tipo "App para computador")
  tokens/<slug>.json   (criado pelo comando autorizar)
"""
import argparse
import datetime as dt
import io
import json
import re
import subprocess
import sys
import time
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parent.parent
import os
CANAIS_JSON = Path(os.environ.get("CAPITAO_CANAIS", RAIZ_REPO / "canais" / "canais.json"))
CRED = Path.home() / ".capitao" / "youtube"
TOKENS = CRED / "tokens"
LOG = CRED / "registro.log"
ESCOPOS = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]
TRAVESSAO = re.compile(r"[—–]|\s-\s")
MIN_W, MIN_H = 2560, 1440
TOLERANCIA_S = 120


def log(msg: str) -> None:
    linha = f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}"
    print(linha)
    try:
        CRED.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    except OSError:
        pass


def carregar_canais() -> dict:
    canais = json.loads(CANAIS_JSON.read_text(encoding="utf-8"))
    local = CRED.parent / "local.json"
    if local.exists():
        canais.update(json.loads(local.read_text(encoding="utf-8")))
    return canais


# ---------------------------------------------------------------- trava

def sondar(mp4: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,width,height:format=duration", "-of", "json", str(mp4)],
        capture_output=True, text=True,
    ).stdout
    dados = json.loads(out or "{}")
    v = next((s for s in dados.get("streams", []) if s.get("codec_type") == "video"), {})
    a = any(s.get("codec_type") == "audio" for s in dados.get("streams", []))
    return {
        "w": int(v.get("width", 0)), "h": int(v.get("height", 0)), "audio": a,
        "dur": float(dados.get("format", {}).get("duration", 0) or 0),
    }


def trava(mp4: Path, info: dict, canal: dict) -> list:
    erros = []
    s = sondar(mp4)
    if s["w"] < MIN_W or s["h"] < MIN_H:
        erros.append(f"resolucao {s['w']}x{s['h']} abaixo de {MIN_W}x{MIN_H}")
    if not s["audio"]:
        erros.append("sem audio")
    dmin, dmax = canal.get("duracao_min"), canal.get("duracao_max")
    if dmin and s["dur"] < dmin * 60 - TOLERANCIA_S:
        erros.append(f"duracao {s['dur'] / 60:.0f} min abaixo de {dmin} min")
    if dmax and s["dur"] > dmax * 60 + TOLERANCIA_S:
        erros.append(f"duracao {s['dur'] / 60:.0f} min acima de {dmax} min")

    titulo = (info.get("titulo") or "").strip()
    desc = info.get("descricao") or ""
    tags = info.get("tags") or []
    if not titulo:
        erros.append("sem titulo")
    if len(titulo) > 100:
        erros.append(f"titulo com {len(titulo)} caracteres (max 100)")
    if len(desc) > 5000:
        erros.append(f"descricao com {len(desc)} caracteres (max 5000)")
    if "<" in titulo + desc or ">" in titulo + desc:
        erros.append("titulo ou descricao com < ou > (o YouTube recusa)")
    if sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0) > 500:
        erros.append("tags passam de 500 caracteres")
    for campo, texto in (("titulo", titulo), ("descricao", desc)):
        if TRAVESSAO.search(texto):
            erros.append(f"{campo} com travessao ou hifen como pontuacao")
    if not info.get("publicar_em"):
        erros.append("sem publicar_em")
    else:
        try:
            quando = dt.datetime.fromisoformat(info["publicar_em"])
            if quando.tzinfo is None:
                erros.append("publicar_em sem fuso (use -04:00 para Campo Grande)")
        except ValueError:
            erros.append(f"publicar_em invalido: {info['publicar_em']}")
    return erros


# ---------------------------------------------------------------- youtube

def servico(slug: str):
    tok = TOKENS / f"{slug}.json"
    if not tok.exists():
        raise SystemExit(f"Canal {slug} nao autorizado. Rode: postar_youtube.py autorizar --canal {slug}")
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    cred = Credentials.from_authorized_user_file(str(tok), ESCOPOS)
    if not cred.valid:
        cred.refresh(Request())
        tok.write_text(cred.to_json())
    return build("youtube", "v3", credentials=cred, cache_discovery=False)


def autorizar(slug: str, canais: dict) -> None:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    segredo = CRED / "client_secret.json"
    if not segredo.exists():
        raise SystemExit(f"Falta {segredo}. Baixe do Google Cloud (credencial OAuth tipo App para computador).")
    nome = canais["canais"][slug]["nome"]
    print(f"Na tela do Google, escolha o canal: {nome}")
    flow = InstalledAppFlow.from_client_secrets_file(str(segredo), ESCOPOS)
    cred = flow.run_local_server(port=0, prompt="consent", access_type="offline")
    yt = build("youtube", "v3", credentials=cred, cache_discovery=False)
    item = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    titulo = item["snippet"]["title"]
    if titulo.strip().lower() != nome.strip().lower():
        raise SystemExit(f"Voce autorizou o canal '{titulo}', mas pediu '{nome}'. Rode de novo e escolha o certo.")
    TOKENS.mkdir(parents=True, exist_ok=True)
    (TOKENS / f"{slug}.json").write_text(cred.to_json())
    (TOKENS / f"{slug}.json").chmod(0o600)
    log(f"autorizado {slug} -> {titulo} ({item['id']})")


def preparar_thumb(pasta: Path, n: str):
    from PIL import Image

    candidatos = [pasta / "Artes" / f"{n}_thumb.{e}" for e in ("png", "jpg", "jpeg")]
    candidatos += [pasta / "Artes" / f"{n}.{e}" for e in ("png", "jpg", "jpeg")]
    origem = next((c for c in candidatos if c.exists()), None)
    if not origem:
        return None
    img = Image.open(origem).convert("RGB")
    w, h = img.size
    alvo = 16 / 9
    if w / h > alvo:
        nw = int(h * alvo)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < alvo:
        nh = int(w / alvo)
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    img = img.resize((1280, 720), Image.LANCZOS)
    for q in (92, 85, 78, 70, 60):
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() < 2 * 1024 * 1024:
            return buf.getvalue()
    return None


def erro_de_cota(e) -> bool:
    texto = str(getattr(e, "content", b"")) + str(e)
    return "quotaExceeded" in texto or "uploadLimitExceeded" in texto or "rateLimitExceeded" in texto


def subir(yt, mp4: Path, info: dict) -> str:
    from googleapiclient.http import MediaFileUpload

    quando = dt.datetime.fromisoformat(info["publicar_em"])
    agora = dt.datetime.now(dt.timezone.utc)
    status = {"selfDeclaredMadeForKids": False, "embeddable": True}
    if quando > agora + dt.timedelta(minutes=15):
        status.update(privacyStatus="private",
                      publishAt=quando.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    else:
        status["privacyStatus"] = "public"
    corpo = {
        "snippet": {
            "title": info["titulo"].strip(),
            "description": info.get("descricao", ""),
            "tags": info.get("tags", []),
            "categoryId": str(info.get("categoria", "10")),
            "defaultLanguage": info.get("idioma", "en"),
            "defaultAudioLanguage": info.get("idioma", "en"),
        },
        "status": status,
    }
    midia = MediaFileUpload(str(mp4), mimetype="video/mp4", chunksize=64 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=corpo, media_body=midia)
    resp, tentativas = None, 0
    while resp is None:
        try:
            prog, resp = req.next_chunk()
            if prog:
                print(f"  {int(prog.progress() * 100)}%", flush=True)
        except Exception as e:  # noqa: BLE001
            if erro_de_cota(e):
                raise
            tentativas += 1
            if tentativas > 6:
                raise
            espera = 2 ** tentativas
            print(f"  falha de rede, tentando de novo em {espera}s: {e}")
            time.sleep(espera)
    return resp["id"]


def enviar(pasta: Path, slug: str, canais: dict, simular: bool) -> int:
    canal = canais["canais"][slug]
    finais = pasta / "Videos finais"
    reg_p = pasta / "enviados.json"
    registro = json.loads(reg_p.read_text()) if reg_p.exists() else {}
    pendentes = []
    for mp4 in sorted(finais.glob("*_video*.mp4")):
        if mp4.name.endswith(".tmp.mp4") or registro.get(mp4.name, {}).get("video_id"):
            continue
        info_p = mp4.with_name(mp4.stem + "_info.json")
        if not info_p.exists():
            log(f"{slug} {mp4.name}: sem {info_p.name}, pulando")
            continue
        pendentes.append((mp4, info_p))
    if not pendentes:
        log(f"{slug}: nada para enviar")
        return 0

    yt = None if simular else servico(slug)
    codigo = 0
    for mp4, info_p in pendentes:
        info = json.loads(info_p.read_text(encoding="utf-8"))
        info.setdefault("idioma", canal.get("idioma_textos", "en"))
        erros = trava(mp4, info, canal)
        if erros:
            log(f"{slug} {mp4.name}: REPROVADO pela trava: {'; '.join(erros)}")
            if simular:
                codigo = codigo or 1
                continue
            registro[mp4.name] = {"reprovado": erros, "em": dt.datetime.now().isoformat(timespec="seconds")}
            codigo = codigo or 1
            continue
        if simular:
            log(f"{slug} {mp4.name}: aprovado (simulacao), agendaria para {info['publicar_em']}: {info['titulo']}")
            continue
        try:
            vid = subir(yt, mp4, info)
        except Exception as e:  # noqa: BLE001
            if erro_de_cota(e):
                log(f"{slug}: cota diaria da API acabou; o restante sobe na proxima execucao")
                reg_p.write_text(json.dumps(registro, ensure_ascii=False, indent=1))
                return 3
            log(f"{slug} {mp4.name}: ERRO no envio: {e}")
            codigo = codigo or 1
            continue
        entrada = {"video_id": vid, "publicar_em": info["publicar_em"], "titulo": info["titulo"],
                   "enviado_em": dt.datetime.now().isoformat(timespec="seconds")}
        n = re.search(r"_video(\d+)$", mp4.stem).group(1)
        thumb = preparar_thumb(pasta, n)
        if thumb:
            from googleapiclient.http import MediaIoBaseUpload
            try:
                yt.thumbnails().set(videoId=vid, media_body=MediaIoBaseUpload(
                    io.BytesIO(thumb), mimetype="image/jpeg")).execute()
                entrada["thumb"] = "ok"
            except Exception as e:  # noqa: BLE001
                entrada["thumb"] = f"falhou: {e}"
        if info.get("playlist_id"):
            try:
                yt.playlistItems().insert(part="snippet", body={"snippet": {
                    "playlistId": info["playlist_id"],
                    "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
                entrada["playlist"] = "ok"
            except Exception as e:  # noqa: BLE001
                entrada["playlist"] = f"falhou: {e}"
        registro[mp4.name] = entrada
        reg_p.write_text(json.dumps(registro, ensure_ascii=False, indent=1))
        log(f"{slug} {mp4.name}: ENVIADO https://youtu.be/{vid} agendado {info['publicar_em']} "
            f"thumb={entrada.get('thumb', 'sem arte')}")
    if not simular:
        reg_p.write_text(json.dumps(registro, ensure_ascii=False, indent=1))
    return codigo


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("autorizar"); a.add_argument("--canal", required=True)
    e = sub.add_parser("enviar"); e.add_argument("pasta"); e.add_argument("--canal", required=True)
    e.add_argument("--simular", action="store_true")
    t = sub.add_parser("enviar-todos"); t.add_argument("--simular", action="store_true")
    sub.add_parser("status")
    args = ap.parse_args()
    canais = carregar_canais()

    if args.cmd == "autorizar":
        autorizar(args.canal, canais)
        return 0
    if args.cmd == "enviar":
        if args.canal not in canais["canais"]:
            raise SystemExit(f"canal desconhecido: {args.canal}")
        return enviar(Path(args.pasta).expanduser(), args.canal, canais, args.simular)
    if args.cmd == "enviar-todos":
        raiz = Path(canais["raiz_canais_mac"]).expanduser()
        if not raiz.is_dir():
            log(f"pasta dos canais nao encontrada: {raiz} (SSD desconectado?)")
            return 1
        pior = 0
        for slug, c in canais["canais"].items():
            if c.get("tipo") != "musica":
                continue
            pasta = raiz / c["pasta"]
            if not (pasta / "Videos finais").is_dir():
                continue
            r = enviar(pasta, slug, canais, args.simular)
            if r == 3:
                return 3
            pior = max(pior, r)
        return pior
    if args.cmd == "status":
        for slug, c in canais["canais"].items():
            if c.get("tipo") == "musica":
                ok = "autorizado" if (TOKENS / f"{slug}.json").exists() else "NAO autorizado"
                print(f"{c['nome']:<25} {ok}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
