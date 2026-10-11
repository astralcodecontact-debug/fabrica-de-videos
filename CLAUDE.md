# Fábrica de vídeos do Capitão

Repositório com as skills, agentes e ferramentas que produzem os vídeos de YouTube de todos os canais do Capitão.

## Regras fixas
* Fale com o Capitão em português do Brasil, curto e direto.
* Nunca use travessão nem hífen como pontuação em nada entregue (títulos, descrições, legendas, roteiros, respostas).
* Imagem e vídeo no mínimo 2K. Nada inventado: fato com fonte, citação real e atribuída, rumor marcado como rumor.
* Canais de música: sobem e agendam sozinhos pelo `ferramentas/postar_youtube.py`, sempre passando pela trava automática. Nunca suba por outro caminho. Vice Report BR: o Capitão envia; os agentes nunca publicam.
* Nunca apague arquivos do Capitão; mova para `tmpm/`.

## Quando o Capitão mandar fotos
Foto (ou link do Canva) com o nome de um canal de música = pedido para entregar o vídeo pronto para postar. Uma foto por vídeo, na ordem enviada. Não pergunte nada que já esteja em `canais/canais.json`. Quem orquestra é a conversa principal:
1. **Mac ou nuvem**: sem `~/.capitao/local.json` ou sem o SSD montado, você está na nuvem e não alcança SSD, render nem envio. Diga numa linha que precisa da sessão do Mac (`bash iniciar.sh`, Remote Control no app) e adiante só o que não depende dele, como conferir pelo conector do Drive quanta música o canal tem.
2. **Fotos para o disco**: subagente não enxerga imagem do chat. Grave antes com `python3 ferramentas/fotos_do_chat.py "<raiz_canais_mac>/<pasta>/Artes" --substituir` (rodando da raiz do repositório); se ele não achar foto, procure o anexo em ~/Downloads ou no caminho citado na mensagem. Link do Canva vai direto para o produtor. Foto abaixo de 2560x1440 (o app reduz anexos): avise e peça o link do Canva ou o original na pasta `Artes` do canal no Drive.
3. **Músicas**: `python3 ferramentas/sincronizar_musicas.py <slug>` traz do Drive (`pasta_drive` do canal, qualquer subpasta) para `<raiz_canais_mac>/<pasta>/Musicas` só o que é novo e mostra quantos minutos há. Se faltar e o Capitão acabou de baixar do Suno, repita com `--extra ~/Downloads --desde-dias 3`.
4. **Produção**: rode o agente `produtor-musica` para o canal com as artes já gravadas, quantos vídeos e para quais dias. Fundo animado (`ferramentas/animar_natureza.py`, protegendo personagem e texto) só se o Capitão pedir movimento. Se faltar só o dia, use o próximo dia de publicação livre do canal.
5. **Entrega**: depois do render, rode o `revisor-youtube` e responda por vídeo com título, descrição (com tracklist), tags, data e hora de publicação e o link do YouTube, ou o motivo de não ter subido.

## Dados pessoais
Nome, cidade, faculdade, e-mail, nome do SSD, caminhos do Mac e link do painel ficam em `~/.capitao/local.json` (modelo em `ferramentas/local.exemplo.json`). Leia esse arquivo quando precisar desses valores e nunca grave nenhum deles no repositório: ele é público.

## Onde está cada coisa
* `canais/canais.json`: fonte única dos canais (pasta, estilo, duração, dias, horário). Mude aqui, não nos agentes.
* `.claude/agents/`: produtor-musica, vice-report-video-longo, estrategista-youtube, revisor-youtube, e os dois originais (organizador-do-capitao, vice-report-pauta-diaria).
* `.claude/commands/`: `/semana-youtube`, `/postar`, `/video-musica`, `/video-gta`, `/estrategia`, `/revisar-video`, `/plano-do-dia`, `/pauta-gta`.
* `.claude/skills/`: as 35 skills do pacote.
* `ferramentas/`: `fotos_do_chat.py` (fotos do chat para `Artes/`), `sincronizar_musicas.py` (Drive para o SSD), `montar_mixes.py` (listas de faixas e tracklist), `renderizar_videos.sh` (render 2K com fade e EQ) e `postar_youtube.py` (envio e agendamento pela API oficial). Credenciais ficam em `~/.capitao/youtube/`, nunca no repositório.
* `plugins/`: marketplace local "capitao" (omniroute-skills, design, postiz).

## Fluxo
`/semana-youtube` lê os canais, vê o que falta e dispara em paralelo um produtor por canal e um pacote por vídeo longo do Vice Report BR, depois passa tudo pelo revisor. Subagentes não chamam outros subagentes: quem orquestra é sempre a conversa principal (os comandos).
