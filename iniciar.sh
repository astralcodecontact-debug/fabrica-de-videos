#!/bin/bash
# Liga a fabrica no Mac: ambiente Python do projeto, Mac acordado e Remote Control.
# Uso: bash iniciar.sh   (dentro da pasta fabrica-de-videos)
set -e
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
command -v ffmpeg >/dev/null || brew install ffmpeg
if [ ! -x .venv/bin/python3 ]; then
  echo "Criando o ambiente Python do projeto (so na primeira vez)..."
  python3 -m venv .venv
  .venv/bin/python3 -m pip install -q --upgrade pip
  .venv/bin/python3 -m pip install -q -r ferramentas/requirements.txt
fi
source .venv/bin/activate
mkdir -p ~/.capitao
[ -f ~/.capitao/local.json ] || echo "Aviso: falta ~/.capitao/local.json (modelo em ferramentas/local.exemplo.json)"
git pull -q --ff-only 2>/dev/null || true
caffeinate -dims -w $$ &
echo "Pronto. Abrindo o Remote Control; a sessao aparece no app Claude Code do celular."
exec claude remote-control
