# Fábrica de vídeos do Capitão

Repositório com as skills, agentes e ferramentas que produzem os vídeos de YouTube de todos os canais do Capitão.

## Regras fixas
* Fale com o Capitão em português do Brasil, curto e direto.
* Nunca use travessão nem hífen como pontuação em nada entregue (títulos, descrições, legendas, roteiros, respostas).
* Imagem e vídeo no mínimo 2K. Nada inventado: fato com fonte, citação real e atribuída, rumor marcado como rumor.
* Canais de música: sobem e agendam sozinhos pelo `ferramentas/postar_youtube.py`, sempre passando pela trava automática. Nunca suba por outro caminho. Vice Report BR: o Capitão envia; os agentes nunca publicam.
* Nunca apague arquivos do Capitão; mova para `tmpm/`.

## Dados pessoais
Nome, cidade, faculdade, e-mail, nome do SSD, caminhos do Mac e link do painel ficam em `~/.capitao/local.json` (modelo em `ferramentas/local.exemplo.json`). Leia esse arquivo quando precisar desses valores e nunca grave nenhum deles no repositório: ele é público.

## Onde está cada coisa
* `canais/canais.json`: fonte única dos canais (pasta, estilo, duração, dias, horário). Mude aqui, não nos agentes.
* `.claude/agents/`: produtor-musica, vice-report-video-longo, estrategista-youtube, revisor-youtube, e os dois originais (organizador-do-capitao, vice-report-pauta-diaria).
* `.claude/commands/`: `/semana-youtube`, `/postar`, `/video-musica`, `/video-gta`, `/estrategia`, `/revisar-video`, `/plano-do-dia`, `/pauta-gta`.
* `.claude/skills/`: as 35 skills do pacote.
* `ferramentas/`: `montar_mixes.py` (listas de faixas e tracklist), `renderizar_videos.sh` (render 2K com fade e EQ) e `postar_youtube.py` (envio e agendamento pela API oficial). Credenciais ficam em `~/.capitao/youtube/`, nunca no repositório.
* `plugins/`: marketplace local "capitao" (omniroute-skills, design, postiz).

## Fluxo
`/semana-youtube` lê os canais, vê o que falta e dispara em paralelo um produtor por canal e um pacote por vídeo longo do Vice Report BR, depois passa tudo pelo revisor. Subagentes não chamam outros subagentes: quem orquestra é sempre a conversa principal (os comandos).
