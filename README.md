# Fábrica de vídeos do Capitão

Agentes do Claude Code que produzem os vídeos de YouTube de todos os canais:

| Canal | Tipo | Agente |
|---|---|---|
| Vice Report BR | GTA 6, narrado, PT-BR | `vice-report-video-longo` (+ `vice-report-pauta-diaria` para Shorts, carrossel e countdown) |
| Chill in Rio | bossa nova | `produtor-musica` |
| Space Jazz Noir | jazz | `produtor-musica` |
| MindForge Studio | ambient para foco | `produtor-musica` (+ skill `mindforge-quote-intro`) |
| Classical Adagio Music | neoclássico calmo | `produtor-musica` |
| Ars Melancholia | neoclássico sombrio | `produtor-musica` |

Todos passam por `estrategista-youtube` (títulos e thumbs) e `revisor-youtube` (checagem antes de subir).

## Como usar
0. No Mac, copie `ferramentas/local.exemplo.json` para `~/.capitao/local.json` e preencha (nome do SSD, pasta do Drive, link do painel). Esse arquivo nunca vai para o Git.
1. Abra o Claude Code nesta pasta (no Mac, para ter acesso ao SSD e ao Drive). Skills, agentes e comandos carregam sozinhos.
2. Comandos:
   * `/semana-youtube` produz a semana de todos os canais em paralelo.
   * `/postar` sobe o que estiver pronto e pendente.
   * `/video-musica ars-melancholia` produz um canal.
   * `/video-gta` monta o próximo vídeo longo do Vice Report BR.
   * `/estrategia chill-in-rio` pesquisa nicho, thumbs e títulos.
   * `/revisar-video <arquivos>` revisão final.
3. Plugins (opcional): `/plugin marketplace add ./plugins` e depois `/plugin install postiz@capitao` (e `design@capitao`, `omniroute-skills@capitao`).
4. Conectores (vidIQ, Canva, Gmail, Drive) não vêm no repositório: adicione com `claude mcp add`.

## Postagem automática (canais de música)
Os vídeos de música sobem e agendam sozinhos logo depois do render, pela API oficial do YouTube. Antes de subir, uma trava confere resolução, duração, áudio, título, descrição, tags e a regra do travessão; o que reprovar não sobe e fica no registro. A thumbnail é a arte do Canva.

Configuração única no Mac:
1. `pip3 install -r ferramentas/requirements.txt`
2. Google Cloud: criar um projeto, ativar a "YouTube Data API v3", configurar a tela de consentimento OAuth (tipo Externo, seu e-mail como usuário de teste) e criar uma credencial OAuth do tipo "App para computador". Baixar o JSON como `~/.capitao/youtube/client_secret.json`.
3. Autorizar cada canal (escolha o canal certo na tela do Google): `python3 ferramentas/postar_youtube.py autorizar --canal ars-melancholia` e repetir para os outros.
4. Pedir a auditoria do projeto à Google ("YouTube API Services audit"). Sem ela, vídeos enviados por projeto novo ficam travados como privados.
5. Reserva diária: `bash ferramentas/instalar_agendamento_mac.sh` (sobe às 3h07 o que ficou pendente por cota ou Mac desligado).
6. Conferir: `python3 ferramentas/postar_youtube.py status` e testar com `--simular`.

Registro de tudo em `~/.capitao/youtube/registro.log`; cada pasta de canal ganha um `enviados.json` para não subir duas vezes.

## Ferramentas
* `ferramentas/montar_mixes.py <pasta do canal> --minutos 120 [--videos 3] [--evitar <canal irmão>] [--so-portugues]`
* `CANAL=<slug> ferramentas/renderizar_videos.sh <nome_saida> ["1 2 3"] [bl|br|tl|tr]` (rodar dentro da pasta do canal; com CANAL sobe sozinho no fim)
* `ferramentas/postar_youtube.py autorizar|enviar|enviar-todos|status [--simular]`

Precisa de `ffmpeg`, `ffprobe` e Python 3.

## Para ajustar
Tudo de canal (duração, horário, pasta) fica em `canais/canais.json`. Falta preencher a duração do Chill in Rio e conferir os nomes das pastas no SSD.

O pacote original veio do zip `capitao-claude-code`; o LEIA-ME dele está em `LEIA-ME-pacote-original.md`.
