#!/usr/bin/env python3
"""Salva em disco as fotos que o Capitao anexou na conversa do Claude Code.

Subagentes nao enxergam imagens do chat; elas so existem na transcricao da sessao
(~/.claude/projects/<pasta do projeto>/<sessao>.jsonl). Este script le a sessao mais
recente do projeto, pega as imagens anexadas pelo Capitao (nao as que o Claude abriu
com ferramentas) e grava como <destino>/1.png, 2.png... na ordem em que chegaram.

Uso:
  python3 fotos_do_chat.py <pasta Artes do canal> [--quantas 3] [--inicio 1] [--substituir]
  python3 fotos_do_chat.py --listar

Sem --quantas: todas as imagens da ultima mensagem que tinha imagem.
--substituir move as artes antigas do mesmo numero (N.*, N_loop.mp4, N_thumb.*) para
<pasta do canal>/tmpm/ antes de gravar; sem ele, se ja existir arte com o numero, para.
O app pode reduzir a foto ao anexar: o script mostra a resolucao e avisa se ficou
abaixo de 2560x1440 (nesse caso, peca o original ou o link do Canva).
"""
import argparse
import base64
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

EXT = {"image/png": "png", "image/jpeg": "jpg", "image/jpg": "jpg", "image/webp": "webp"}
MIN_W, MIN_H = 2560, 1440


def sessao_atual() -> Path:
    base = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / "projects"
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(Path.cwd()))
    for pasta in (base / slug, base):
        arquivos = [p for p in pasta.glob("*.jsonl" if pasta != base else "*/*.jsonl")]
        if arquivos:
            return max(arquivos, key=lambda p: p.stat().st_mtime)
    raise SystemExit(f"nao achei transcricao de sessao em {base}")


def imagens_por_mensagem(jsonl: Path) -> list:
    """Lista de (horario, [(media_type, bytes), ...]) das mensagens do Capitao com imagem."""
    msgs = []
    for linha in jsonl.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if d.get("type") != "user" or d.get("isSidechain") or d.get("isMeta"):
            continue
        conteudo = (d.get("message") or {}).get("content")
        if not isinstance(conteudo, list):
            continue
        imgs = []
        for bloco in conteudo:  # so blocos do topo: imagens de tool_result nao contam
            if not isinstance(bloco, dict):
                continue
            src = bloco.get("source") or {}
            if bloco.get("type") == "image" and src.get("type") == "base64":
                imgs.append((src.get("media_type", "image/png"), base64.b64decode(src["data"])))
        if imgs:
            msgs.append((d.get("timestamp", "?"), imgs))
    return msgs


def resolucao(p: Path) -> tuple:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=p=0:s=x", str(p)],
        capture_output=True, text=True,
    ).stdout.strip()
    try:
        w, h = out.split("x")[:2]
        return int(w), int(h)
    except ValueError:
        return 0, 0


def antigas(destino: Path, n: int) -> list:
    return [p for p in destino.glob(f"{n}*")
            if re.fullmatch(rf"{n}(_loop|_thumb)?\.[A-Za-z0-9]+", p.name)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("destino", nargs="?")
    ap.add_argument("--quantas", type=int)
    ap.add_argument("--inicio", type=int, default=1)
    ap.add_argument("--substituir", action="store_true")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--sessao", help="caminho de um .jsonl especifico")
    a = ap.parse_args()

    jsonl = Path(a.sessao).expanduser() if a.sessao else sessao_atual()
    msgs = imagens_por_mensagem(jsonl)
    if a.listar or not a.destino:
        print(f"sessao: {jsonl}")
        for quando, imgs in msgs:
            print(f"{quando}: {len(imgs)} imagem(ns)")
        return 0
    if not msgs:
        print("nenhuma foto anexada nesta sessao", file=sys.stderr)
        return 1

    if a.quantas:
        fotos = [img for _, imgs in msgs for img in imgs][-a.quantas:]
    else:
        fotos = msgs[-1][1]

    destino = Path(a.destino).expanduser()
    destino.mkdir(parents=True, exist_ok=True)
    numeros = range(a.inicio, a.inicio + len(fotos))
    ocupadas = [p for n in numeros for p in antigas(destino, n)]
    if ocupadas and not a.substituir:
        nomes = ", ".join(p.name for p in ocupadas)
        print(f"ja existem artes com esses numeros ({nomes}); use --substituir "
              "para mover as antigas para tmpm/ ou --inicio para outro numero", file=sys.stderr)
        return 2
    if ocupadas:
        lixo = destino.parent / "tmpm" / f"Artes_{dt.datetime.now():%Y%m%d_%H%M%S}"
        lixo.mkdir(parents=True, exist_ok=True)
        for p in ocupadas:
            p.rename(lixo / p.name)
        print(f"artes antigas movidas para {lixo}")

    pequenas = 0
    for n, (tipo, dados) in zip(numeros, fotos):
        alvo = destino / f"{n}.{EXT.get(tipo, 'png')}"
        alvo.write_bytes(dados)
        w, h = resolucao(alvo)
        baixa = w < MIN_W or h < MIN_H
        pequenas += baixa
        print(f"{alvo}: {w}x{h}{'  ABAIXO DE 2560x1440' if baixa else ''}")
    if pequenas:
        print(f"aviso: {pequenas} foto(s) abaixo de 2K; o app reduz o anexo. "
              "Melhor o link do Canva ou a foto original na pasta Artes do Drive.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
