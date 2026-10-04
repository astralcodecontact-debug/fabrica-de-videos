---
name: analisar-thumbs
description: "Baixar e analisar visualmente as thumbnails dos vídeos que mais estouram em cada nicho dos canais de música do Capitão (Chill in Rio, Space Jazz Noir, MindForge Studio, Mind At Ease, Ars Melancholia), montar painéis lado a lado e entregar a fórmula visual de cada canal com um briefing para o Canva. Use quando pedirem para analisar, comparar ou estudar thumbnails, ou para revisar uma thumbnail nova antes de publicar."
---

# Analisar thumbnails dos canais de música

Escreva para o Capitão em português do Brasil, direto. Nunca use travessão nem hífen como pontuação.

## Por que roda no Mac
A rede da sessão na nuvem bloqueia as imagens do YouTube (i.ytimg.com). Baixe sempre pelo Mac do Capitão com `mcp__remote-devices__device_bash` (usa a internet dele) e traga só os painéis prontos para olhar com `device_stage_files` e Read. Se as ferramentas do Mac não estiverem disponíveis, pare e peça para ele abrir a conversa ligada ao Mac ou mandar prints.

## Pasta no Mac
`~/Documents/Canais de Musica/_thumbs_referencia/<canal>/` com as imagens baixadas, `painel_1.jpg`, `painel_2.jpg` e `analise.md`.

## Passo a passo

### 1. Escolher os vídeos
* Para cada canal, use o vidIQ (`vidiq_outliers`, contentType long, publishedWithin threeMonths, minViews 3000) com as palavras do nicho:
  * Chill in Rio: "bossa nova"
  * Space Jazz Noir: "noir jazz", "late night jazz", "space jazz"
  * MindForge Studio: "focus music playlist", "flowstate"
  * Mind At Ease: "neoclassical piano reading", "calm classical piano"
  * Ars Melancholia: "dark academia"
* Descarte o que não é música (tutorial, game, vlog) e covers de músicas famosas. Fique com 20 a 25 vídeos por nicho, priorizando breakoutScore alto e canais pequenos que estouraram.
* Inclua também os 5 vídeos mais recentes do próprio canal (`vidiq_channel_videos`, popular false) para comparar.
* Ponto de partida (vídeos que estouraram até outubro de 2026, já levantados):
  * Bossa nova: kEw4URp6qFU, nlEjegwaKx8, VBQSv0iR9QE, AEfcEfbnRXw, vUfcKBqSobA, 2xhuxRq9af4, _p4RfbmzUKE, dXwVsQkFtgw; do canal: Ap1IPS9tgpg, Y6Baz0Ejjho, 7wEpOzu9380, 62s0WyvZ3as, gXF6j-g4Bso
  * Noir jazz: UJbkqP-8Mus, KB14lLj9Y4s, 7SrFkKq8jiM, lXsUNnF55Uc, xmSo_9ZrPlI, IqzLKvsCS8E, 9FQcHbT-sDA, P7psziQcTPI; do canal: pVGO9ck_pu0, WVRnVIuHNKo, bR3PyG45ypE
  * Foco: wdDhTr_M7kA, A-R177XUPfw, Nh6E6PJLzfA, mppFzN1AiQo, Xb1YOylgP1k, -L3JgDVrbh8, Zg8k-NE3qSY, HE4LqxbA040; do canal: 98SSjxC4ULM, Czn5ENXa3Y0, b7unGA8Nb9E, kJbIE0h6HZo
  * Neoclássico calmo: b9IAmMK3REE, jHFT87DZrrM, 3Ezftu7dR84, zwr3w6yiwmA, iDNSLgq6uQU, 4gtS-JDnSP4, jvhw8fEBjrk, aH3JBdcW8po; do canal: rhkygMzxngw, sj0zliVOCWY
  * Dark academia: vgZCA2XJk8s, CdMtMeoWETI, 757EXr7LkL8, Z5HMV-w4SjM, ynKNLLi2h7w, qz3c5GlZ2Pw, V-HaIXHBaDM; do canal: yCBXVbyWjhc, Q4jcwHqCpAA, B6fYdtFPUeo, K2AU_SuFE9o

### 2. Baixar no Mac
Para cada id, numa pasta do canal (prefixe com `c_` os do próprio canal):
```
curl -sfL -o "<n>_<id>.jpg" "https://i.ytimg.com/vi/<id>/maxresdefault.jpg" || curl -sfL -o "<n>_<id>.jpg" "https://i.ytimg.com/vi/<id>/hqdefault.jpg"
```
Confira o tamanho dos arquivos: um maxres inexistente vem como imagem cinza pequena; nesse caso use o hqdefault.

### 3. Montar os painéis (ffmpeg no Mac)
Grade de 4 colunas, cada thumb em 480x270, com o número escrito no canto para você citar na análise:
```
ffmpeg -y -pattern_type glob -i '*.jpg' -vf "scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2,drawtext=text='%{n}':x=8:y=8:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6,tile=4x4" -frames:v 1 painel_1.jpg
```
Se passar de 16 imagens, faça um segundo painel com o restante. Monte também um painel só com as do próprio canal. Traga os painéis com `device_stage_files` e olhe cada um com Read. Abra uma thumb inteira quando precisar ver detalhe de texto ou fonte.

### 4. Analisar (para cada nicho)
Olhe de verdade e anote, citando o número das thumbs:
* **Estilo da imagem:** foto real, pintura, ilustração, anime, 3D, foto vintage com grão.
* **Assunto e composição:** pessoa ou objeto, onde fica (centro, terço), plano aberto ou fechado, quanto espaço vazio.
* **Pessoas e rosto:** tem gente? de frente, de costas, de perfil? expressão?
* **Paleta e luz:** cores dominantes, quente ou fria, contraste, hora do dia.
* **Texto:** tem ou não; quantas palavras; fonte (serifada, script, condensada); posição; tamanho; se lê em tamanho de celular.
* **Elementos que se repetem:** vinil, xícara, livro, vela, chuva, janela, piano, sax, neon, planeta.
* **Marca:** logo do canal, selo, padrão de série.
* **O que os que mais estouraram têm em comum** e o que os fracos têm diferente.
* **Comparação com o canal do Capitão:** o que já está alinhado e o que destoa.

### 5. Entregar
Salve `analise.md` na pasta do canal e responda ao Capitão com, para cada canal:
1. A fórmula visual em 3 a 5 linhas.
2. Os 3 exemplos mais fortes (número e título).
3. O que mudar nas thumbs dele.
4. Um briefing pronto para o Canva: cena, enquadramento, paleta, texto (se tiver, com fonte e posição) e o que evitar.
Use o painel como referência de estilo, nunca para copiar arte de outro canal.

## Revisar uma thumbnail nova
Quando o Capitão mandar uma thumb (ou o nome do design no Canva), coloque-a num painel junto com 7 das referências do nicho, todas em 480x270, e diga se ela se destaca no meio delas, se o texto lê em tamanho pequeno e o que ajustar.
