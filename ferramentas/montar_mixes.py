#!/usr/bin/env python3
"""Monta as listas de faixas dos videos de um canal de musica.

Para cada video: embaralha as faixas de Musicas/, nunca repete o mesmo nome base
no mesmo video (ignora sufixos como " (1)" e " copy"), para ao atingir a duracao
alvo e grava lista_videoN.txt (formato concat do ffmpeg) e tracklist_videoN.txt
(H:MM:SS Nome).

Uso:
  python3 montar_mixes.py <pasta_do_canal> --minutos 120 [--videos 3]
      [--evitar <pasta_do_canal_irmao>] [--so-portugues] [--semente 7]

--evitar le as listas lista_video*.txt de outro canal (Classical Adagio e
Ars Melancholia dividem faixas) e nao usa nenhuma faixa que ja esta la.
--so-portugues aceita so faixas cujo nome tem cara de portugues (Chill in Rio).
"""
import argparse
import json
import random
import re
import subprocess
import sys
from pathlib import Path

EXTS = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"}
SUFIXO = re.compile(r"(\s*\(\d+\)|\s+copy(\s+\d+)?)$", re.IGNORECASE)
PT_MARCAS = re.compile(
    r"[ãõçáéíóúâêô]|\b(de|da|do|das|dos|na|no|em|meu|minha|amor|noite|mar|sol|"
    r"saudade|praia|cidade|coração|tarde|manhã|chuva|samba|bossa|rio)\b",
    re.IGNORECASE,
)


def nome_base(p: Path) -> str:
    base = p.stem.strip()
    while True:
        novo = SUFIXO.sub("", base).strip()
        if novo == base:
            return base.lower()
        base = novo


def duracao(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True,
    ).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def hms(seg: float) -> str:
    s = int(seg)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def faixas_usadas(pasta_irma: Path) -> set:
    usadas = set()
    for lista in pasta_irma.glob("lista_video*.txt"):
        for linha in lista.read_text(encoding="utf-8").splitlines():
            m = re.match(r"file '(.+)'$", linha.strip())
            if m:
                usadas.add(nome_base(Path(m.group(1).replace("'\\''", "'"))))
    return usadas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--minutos", type=float, required=True)
    ap.add_argument("--videos", type=int, default=3)
    ap.add_argument("--evitar")
    ap.add_argument("--so-portugues", action="store_true")
    ap.add_argument("--semente", type=int)
    a = ap.parse_args()

    pasta = Path(a.pasta).expanduser()
    musicas = pasta / "Musicas"
    if not musicas.is_dir():
        print(f"ERRO: nao achei {musicas}", file=sys.stderr)
        return 1

    cache_p = pasta / ".duracoes.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}

    proibidas = faixas_usadas(Path(a.evitar).expanduser()) if a.evitar else set()
    faixas = {}
    for p in sorted(musicas.iterdir()):
        if p.suffix.lower() not in EXTS or p.name.startswith("."):
            continue
        base = nome_base(p)
        if base in proibidas or base in faixas:
            continue
        if a.so_portugues and not PT_MARCAS.search(p.stem):
            continue
        if p.name not in cache:
            cache[p.name] = duracao(p)
        if cache[p.name] > 0:
            faixas[base] = p
    cache_p.write_text(json.dumps(cache, ensure_ascii=False, indent=1))

    alvo = a.minutos * 60
    total_disp = sum(cache[p.name] for p in faixas.values())
    if total_disp < alvo:
        print(f"ERRO: so ha {hms(total_disp)} de musica utilizavel, alvo {hms(alvo)}",
              file=sys.stderr)
        return 2

    rnd = random.Random(a.semente)
    resumo = []
    for v in range(1, a.videos + 1):
        ordem = list(faixas.values())
        rnd.shuffle(ordem)
        t, escolhidas = 0.0, []
        for p in ordem:
            if t >= alvo:
                break
            escolhidas.append((t, p))
            t += cache[p.name]
        with open(pasta / f"lista_video{v}.txt", "w", encoding="utf-8") as f:
            for _, p in escolhidas:
                rel = f"Musicas/{p.name}".replace("'", "'\\''")
                f.write(f"file '{rel}'\n")
        with open(pasta / f"tracklist_video{v}.txt", "w", encoding="utf-8") as f:
            for ini, p in escolhidas:
                f.write(f"{hms(ini)} {SUFIXO.sub('', p.stem).strip()}\n")
        resumo.append(f"video{v}: {len(escolhidas)} faixas, {hms(t)}")
    print("\n".join(resumo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
