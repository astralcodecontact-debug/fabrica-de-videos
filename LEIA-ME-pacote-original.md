# Pacote do Capitão para o Claude Code

## Como instalar (Mac)
1. Descompacte o zip numa pasta fixa (ex: ~/capitao-claude-code).
2. No Terminal: `bash ~/capitao-claude-code/instalar.sh`
3. Plugins (opcional), dentro do Claude Code:
   `/plugin marketplace add ~/capitao-claude-code/plugins`
   `/plugin install omniroute-skills@capitao`
   `/plugin install design@capitao`
   `/plugin install postiz@capitao`
4. Reinicie o Claude Code. Confira com `/agents` e digitando `/` para ver os comandos.

## O que tem aqui
- skills/ : 35 skills (Vice Report, canais de música, design, HyperFrames, carrosséis etc.). Vão para ~/.claude/skills.
- agents/ : 2 agentes, que eram suas tarefas agendadas.
  - organizador-do-capitao (plano do dia e painel Diário de Bordo)
  - vice-report-pauta-diaria (pauta, countdown, carrossel, Shorts e vídeo longo)
- commands/ : atalhos `/plano-do-dia` e `/pauta-gta` que chamam os agentes.
- plugins/ : omniroute-skills, design e postiz, num marketplace local chamado "capitao".

## O que ficou de fora e por quê
- docx, pdf, pptx, xlsx: são skills da Anthropic com licença própria. Instale pelo marketplace oficial:
  `/plugin marketplace add anthropics/skills` e depois `/plugin install document-skills@anthropic-agent-skills`
- computer-use, chrome-browser, built-in-browser, docs, import-memory, morning e cowork-plugin-management: só funcionam no app Claude (Cowork). No Claude Code, o Chrome entra com `claude --chrome`.

## Sobre os agentes
- As tarefas agendadas continuam rodando na nuvem todo dia (6h48 e 7h18). Este pacote não desliga nada.
- No Claude Code os agentes rodam quando você chama. Cada um tem no topo uma nota de adaptação (caminhos locais do Mac no lugar das ferramentas remotas, Playwright, Chrome).
- Conectores (vidIQ, Canva, Gmail, Drive) não vêm no pacote: adicione no Claude Code com `claude mcp add` se quiser usar.
