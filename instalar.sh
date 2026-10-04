#!/bin/bash
# Instala skills, agentes e comandos deste repositório no Claude Code do usuário (~/.claude),
# para usar fora desta pasta. Dentro do repositório eles já carregam sozinhos pela pasta .claude/.
set -e
cd "$(dirname "$0")"
mkdir -p ~/.claude/skills ~/.claude/agents ~/.claude/commands
cp -R .claude/skills/* ~/.claude/skills/
cp .claude/agents/*.md ~/.claude/agents/
cp .claude/commands/*.md ~/.claude/commands/
echo "Pronto: $(ls .claude/skills | wc -l | tr -d ' ') skills, $(ls .claude/agents | wc -l | tr -d ' ') agentes e $(ls .claude/commands | wc -l | tr -d ' ') comandos em ~/.claude"
echo "Atenção: fora do repositório os agentes não acham canais/canais.json nem ferramentas/. Prefira abrir o Claude Code nesta pasta."
echo "Plugins: no Claude Code rode  /plugin marketplace add $(pwd)/plugins"
