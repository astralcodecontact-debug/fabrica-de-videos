---
name: "vice-report-video-narrado"
description: "Narrar em PT-BR com o Matheus do ElevenLabs um vídeo longo de canal gringo, sincronizar a fala com as cenas e gerar título, descrição, capítulos e tags pro YouTube."
---

# Vídeo longo narrado (Vice Report BR)

Use quando o Capitão mandar um vídeo (geralmente de canal gringo, sem áudio) + a transcrição e pedir para narrar no ElevenLabs e encaixar com as cenas.

Regra fixa de texto: nunca usar travessão nem hífen como pontuação em nada entregue ao Capitão.

## Ferramentas no Mac
`~/Documents/Vice Report BR/_ferramentas/video_narrado/`
* `cortes_narracao.py`: acha os pontos de corte entre parágrafos dentro de cada mp3.
* `gerar_render.py`: gera o `render.sh` que renderiza os segmentos no próprio Mac.
Traga com device_stage_files quando precisar rodar no container.

## Passo a passo

### 1. Conferir o vídeo certo
* O vídeo grande costuma estar em `~/Downloads` (webm 4K). Antes de tudo, tire 5 frames em pontos diferentes e confira se o conteúdo bate com a transcrição. Já aconteceu de o arquivo anexado ser outro (um podcast). Se não bater, procure nos Downloads o vídeo que bate e avise o Capitão.
* Arquivos acima de ~400 MB não passam pelo stage: trabalhe com o ffmpeg do Mac (device_bash). Processos em segundo plano morrem ao fim de cada chamada; rode em primeiro plano em lotes de até ~170 s.

### 2. Texto da narração
* Remova títulos de capítulos e marcações; deixe só a fala, em português natural de YouTuber BR ("mano", "bora lá"), trocando o nome do canal original por Vice Report.
* Divida em partes de até ~3.500 caracteres, uma por capítulo, mantendo os parágrafos (cada parágrafo costuma corresponder a um clipe).
* Salve `narracao_partes.txt` e a lista em JSON (um texto por parte, parágrafos separados por \n).

### 3. ElevenLabs (Claude in Chrome)
* Voz: **Matheus, Youthful, Cheery and Bright**, modelo **Eleven v4** (o Capitão normalmente já deixa a aba aberta com a voz).
* Insira o texto SEM quebras de linha (parágrafos unidos com espaço; com \n o contador só registra o 1º parágrafo):
  `window.__setText=function(t){const ed=document.querySelector('[contenteditable="true"]');ed.focus();document.execCommand('selectAll');document.execCommand('insertText',false,t);return ed.innerText.length}`
* Confira o contador "N / 10,000 characters" (zoom na tela) antes de gerar.
* Clique real em Generate speech, espere (~30 a 60 s), clique real no download da Generation 1. Se o ícone ainda estiver girando, espere e clique de novo. Se o Chrome bloquear downloads múltiplos, peça para o Capitão permitir sempre.
* No Mac, copie o `ElevenLabs_*Youthful*.mp3` mais recente de Downloads para `Videos/<projeto>/narracao/parteN.mp3`. Confira por md5 que não é repetido.

### 4. Mapa de cenas
* No Mac: frames a 2 fps, 240 px (`ffmpeg -t 430 ... fps=2,scale=240:-1` e depois `-ss 430`), empacote em tar e traga ao container.
* Monte folhas de contato (8x6, um frame a cada 3 s, com o tempo escrito) e olhe com Read.
* Para cada parágrafo, ache onde começa a cena que ele descreve ("próximo clipe", nome de carro, personagem, mecânica). Ordem sempre igual à do vídeo.
* Ajuste cada início ao corte de cena mais próximo (diferença entre frames, ±2 s).
* Pode pular trechos que não têm nada a ver com a fala daquele bloco.

### 5. Sincronizar
* `python3 cortes_narracao.py partes.json <pasta mp3> cortes.json` dá os cortes por parágrafo.
* Monte `segs.json`: cada segmento = trecho do mp3 (a0, a1) + trechos do vídeo (ranges).
* Fator = duração do áudio / duração do vídeo. Mantenha entre ~0,75 e ~1,3 (o vídeo acelera ou desacelera, a narração nunca muda). Se sair disso, mexa nos limites das cenas.
* `python3 gerar_render.py segs.json "<video no Mac>" "<pasta do projeto no Mac>" > render.sh`, mande ao Mac e rode `bash render.sh 1 2 3 ...` em lotes (~2x tempo real).
* Junte com concat demuxer (`-c copy -movflags +faststart`). Saída 1920x1080, 30 fps, H.264 CRF 20, AAC 192k, fade no início e no fim.
* Confira: duração de vídeo e áudio iguais, e uma tira de 12 frames em tempos-chave batendo com o que a narração diz.
* Apague as pastas temporárias (_segs, frames) depois.

### 6. Textos do YouTube
Salve `youtube_textos.txt` ao lado do vídeo com:
* Título principal + 2 alternativos (gancho forte, até ~70 caracteres).
* Descrição: gancho, resumo do que o vídeo mostra, data de lançamento do GTA 6, chamada para like/inscrição, pergunta para os comentários.
* Capítulos calculados pela linha do tempo real do vídeo final (soma das durações dos segmentos), começando em 0:00.
* 5 hashtags e ~20 tags.
Mande o texto pronto no chat também.

## Entrega
Vídeo final em `Documents/Vice Report BR/Videos/<projeto>/<NOME>_narrado_PTBR.mp4`. Avise duração, onde está e qualquer cena cortada ou ajuste feito. Sem música de fundo, a não ser que o Capitão peça.