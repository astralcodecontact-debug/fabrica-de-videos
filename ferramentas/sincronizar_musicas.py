#!/usr/bin/env python3
"""Traz para <raiz_canais_mac>/<pasta do canal>/Musicas as faixas novas de um canal.

Procura audio, em qualquer subpasta, em:
  1. <drive_musicas_mac>/<pasta_drive do canal>   (Drive para computador, sincronizado)
  2. pastas extras passadas com --extra (ex. ~/Downloads, para faixas recem baixadas do Suno)
Copia so o que ainda nao existe em Musicas/, uma copia por nome base
("Night Train Nap (1).mp3" e "Night Train Nap.mp3" contam como a mesma faixa),
ignora as subpastas Artes, Loops e tmpm e os arquivos "._" do macOS,
e nunca sobrescreve nem apaga nada.
No fim mostra quantas faixas e quantos minutos o canal tem para montar os mixes.

Uso:
  python3 sincronizar_musicas.py <slug> [--extra ~/Downloads --desde-dias 7] [--simular]
"""
import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_mixes import EXTS, duracao, hms, nome_base  # noqa: E402

RAIZ_REPO = Path(__file__).resolve().parent.parent
CANAIS_JSON = Path(os.environ.get("CAPITAO_CANAIS", RAIZ_REPO / "canais" / "canais.json"))
LOCAL_JSON = Path(os.environ.get("CAPITAO_LOCAL", Path.home() / ".capitao" / "local.json"))


def carregar_canais() -> dict:
    canais = json.loads(CANAIS_JSON.read_text(encoding="utf-8"))
    if LOCAL_JSON.exists():
        canais.update(json.loads(LOCAL_JSON.read_text(encoding="utf-8")))
    return canais


IGNORAR = {"artes", "loops", "tmpm"}


def audios(pasta: Path, desde: float = 0.0, subpastas: bool = True):
    # nome sem sufixo primeiro: entre "X.mp3" e "X (1).mp3" fica o "X.mp3"
    todos = pasta.rglob("*") if subpastas else pasta.iterdir()
    for p in sorted(todos, key=lambda p: (str(p.parent), nome_base(p), len(p.name), p.name)):
        if IGNORAR & {d.lower() for d in p.relative_to(pasta).parts[:-1]}:
            continue
        if (p.is_file() and p.suffix.lower() in EXTS and not p.name.startswith(".")
                and p.stat().st_mtime >= desde):
            yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--extra", action="append", default=[],
                    help="outra pasta para procurar faixas (pode repetir)")
    ap.add_argument("--desde-dias", type=float,
                    help="nas pastas extras, so arquivos modificados nos ultimos N dias")
    ap.add_argument("--simular", action="store_true")
    a = ap.parse_args()

    canais = carregar_canais()
    canal = canais["canais"].get(a.slug)
    if not canal or canal.get("tipo") != "musica":
        print(f"ERRO: canal de musica '{a.slug}' nao existe em {CANAIS_JSON}", file=sys.stderr)
        return 1
    if str(canais.get("raiz_canais_mac", "")).startswith("<"):
        print(f"ERRO: falta {LOCAL_JSON} (modelo em ferramentas/local.exemplo.json); "
              "rode no Mac", file=sys.stderr)
        return 1

    destino = Path(canais["raiz_canais_mac"]).expanduser() / canal["pasta"] / "Musicas"
    if not destino.parent.is_dir():
        print(f"ERRO: nao achei a pasta do canal {destino.parent} (SSD conectado?)",
              file=sys.stderr)
        return 1

    origens = []
    drive = Path(str(canais.get("drive_musicas_mac", ""))).expanduser()
    pasta_drive = drive / canal.get("pasta_drive", canal["pasta"])
    if pasta_drive.is_dir():
        origens.append((pasta_drive, 0.0))
    else:
        print(f"aviso: nao achei a pasta do Drive {pasta_drive}")
    desde = time.time() - a.desde_dias * 86400 if a.desde_dias else 0.0
    for e in a.extra:
        p = Path(e).expanduser()
        if p.is_dir():
            origens.append((p, desde))
        else:
            print(f"aviso: pasta extra nao existe: {p}")

    if not a.simular:
        destino.mkdir(exist_ok=True)
    atuais = list(audios(destino, subpastas=False)) if destino.is_dir() else []
    ja_tem = {nome_base(p) for p in atuais}
    copiadas = []
    for pasta, corte in origens:
        for p in audios(pasta, corte):
            base = nome_base(p)
            alvo = destino / p.name
            if base in ja_tem or alvo.exists():
                continue
            ja_tem.add(base)
            copiadas.append(p)
            if not a.simular:
                tmp = alvo.with_name(alvo.name + ".parcial")
                shutil.copy2(p, tmp)
                tmp.rename(alvo)
    for p in copiadas:
        print(f"{'copiaria' if a.simular else 'copiada'}: {p}")

    # mesma conta do montar_mixes.py: uma faixa por nome base, cache em .duracoes.json
    cache_p = destino.parent / ".duracoes.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    unicas = {}
    for p in (audios(destino, subpastas=False) if destino.is_dir() else []):
        unicas.setdefault(nome_base(p), p)
    for p in unicas.values():
        if p.name not in cache:
            cache[p.name] = duracao(p)
    if unicas and not a.simular:
        cache_p.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
    total = sum(cache.get(p.name, 0.0) for p in unicas.values())
    print(f"{len(copiadas)} faixas novas; {destino} tem {len(unicas)} faixas, {hms(total)} de musica")
    if canal.get("duracao_min") and not canal.get("repetir_faixas"):
        falta = canal["duracao_min"] * 60 - total
        if falta > 0:
            print(f"aviso: para 1 video sem repetir faixa faltam {hms(falta)} de musica")
    return 0


if __name__ == "__main__":
    sys.exit(main())
