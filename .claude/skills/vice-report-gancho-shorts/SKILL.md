---
name: "vice-report-gancho-shorts"
description: "Criar um gancho inicial viral (intro narrada pelo Matheus do ElevenLabs, texto animado e efeitos) para Shorts do Vice Report BR, mais legendas e hashtags para TikTok, Reels e YouTube Shorts."
---

# Gancho viral para Shorts (Vice Report BR)

Use quando o Capitão mandar um Short (normalmente feito no Wizard AI) e pedir o hook/intro, ou legenda e hashtags para as redes.

Regra fixa de texto: nunca usar travessão nem hífen como pontuação em nada entregue ao Capitão.

## Ferramentas no Mac
`~/Documents/Vice Report BR/_ferramentas/hook_shorts/`: `text.html`, `render_text.js`, `fonts/` (Archivo, Anton, Bodoni, Inter).
Traga para o container com device_stage_files; rode `npm i playwright` (Chromium já está em /opt/pw-browsers; não rode playwright install).
`node render_text.js saida.png "texto com *destaque*" [kicker] [fs] [bottom] [pos=top] [topv]` gera PNG 1080x1920 transparente: marca VICE REPORT BR, título condensado em caixa alta, destaque em bloco degradê roxo e rosa, degradê escuro embaixo (ou em cima com pos=top).

Pastas: originais em `Shorts/1 Para editar/`, prontos em `Shorts/2 Prontos/` (vídeo `<NOME>_com_gancho.mp4` + `<NOME>_textos.txt`), áudios do gancho em `Shorts/_narracoes/`.

## Passo a passo
1. **Entender o Short**: extraia frames (folha de contato) e leia as legendas queimadas para saber o tema e o melhor momento.
2. **Propor o gancho**: 2 ou 3 opções de frase de 2 a 4 s, em pergunta ou afirmação que gere curiosidade e que o vídeo cumpra (nada enganoso). Mostre ao Capitão a escolhida e siga.
3. **Narração**: ElevenLabs no Claude in Chrome, voz **Matheus, Youthful, Cheery and Bright**, Eleven v4. Mesmo método de inserir texto e baixar do skill vice-report-video-narrado (`window.__setText`, clique real em Generate e no download). Acelere com `atempo` 1.1 a 1.15 se precisar caber no tempo.
4. **Visual do gancho** (3 a 5 s, 1080x1920, 30 fps):
   * Fundo: arte oficial 4K da biblioteca `Documents/Vice Report BR/Imagens GTA 6/` (prefira versões _phone ou _portrait da pasta 11), com movimento `zoompan` lento ou cortes rápidos entre 2 ou 3 imagens ligadas ao tema.
   * Texto: PNGs do `render_text.js` sobrepostos com overlay, entrando em sequência (palavra chave com destaque).
   * Som: whoosh na entrada e boom no impacto, sintetizados com `lavfi` (ruído filtrado com envelope; seno grave com decay), mixados abaixo da voz.
5. **Montar**: concatene gancho + Short original, ambos 1080x1920, 30 fps, AAC 48 kHz. Confira o ponto de emenda e o volume.
6. **Textos**: para TikTok, Instagram Reels e YouTube Shorts: título/gancho, legenda curta com pergunta para comentar e menção a @vicereportbr, 8 a 15 hashtags (GTA6, GTAVI, Rockstar, ViceCity, Leonida...). Salve em `<NOME>_textos.txt` e mande no chat.
7. **Salvar**: device_commit_files (limite 20 MB por arquivo; se passar, concatene no próprio Mac com o ffmpeg dele) e envie o vídeo com SendUserFile para o Capitão ver.

## Qualidade
Só imagens 2K ou 4K. O gancho precisa ser verdadeiro em relação ao conteúdo. O Capitão não quer discussão de copyright: faça o que ele pediu.