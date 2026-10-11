---
name: "domingo-canais-musica"
description: "Produção semanal (domingo) dos vídeos dos canais de música do Capitão: ele manda as fotos, Claude sincroniza músicas no SSD, renderiza 2K com fade e EQ no Mac, sobe e agenda no YouTube."
---

# Domingo: vídeos dos canais de música

O Capitão só manda as fotos e diz o canal. Claude faz o resto sem pedir nada além do necessário. Siga exatamente este caminho; os outros já falharam.

## Canais
Fonte única: `canais/canais.json` (duração, dias, horário, pasta no SSD e `pasta_drive`). A tabela é só referência rápida.

| Canal | Estilo | Duração | Horário (Campo Grande) |
|---|---|---|---|
| Chill in Rio | bossa nova (só faixas com nome em português) | padrão do canal | padrão do canal |
| Space Jazz Noir | jazz | 2h | 18h |
| MindForge Studio | ambient | 2h15 a 2h30 | 8h |
| Classical Adagio Music (@ClassicalAdagioMusic) | neoclássico relax acadêmico | 2h | 18h30 |
| Ars Melancholia | neoclássico sombrio | 2h | 19h |
| Snoopy Loves Music | lo-fi (pode repetir faixa) | 1h30 | 18h |

Publicação seg, qua, sex. Classical Adagio e Ars Melancholia compartilham faixas (ordem diferente, nunca a mesma faixa nos dois na mesma semana). Primeiro vídeo de canal novo: rascunho privado até o Capitão aprovar.

## Não tente (já falhou)
- Baixar de Drive ou Canva pelo Bash da nuvem ou pelo device_bash: rede bloqueada.
- Renderizar no device_bash: VM lenta e mata processos a cada chamada.
- Filesystem MCP do Mac: erro de schema.

## Fluxo
Roda no Mac (sessão do Claude Code aberta com `bash iniciar.sh`, falando pelo app via Remote Control). Na nuvem não há SSD, render nem envio.
1. **Fotos**: subagente não enxerga imagem do chat. A conversa principal grava com `python3 ferramentas/fotos_do_chat.py "<raiz_canais_mac>/<pasta>/Artes" --substituir` (vira 1, 2, 3 na ordem enviada; artes antigas vão para `tmpm/`). Link do Canva: exportar 2560x1440 pelo conector. Foto abaixo de 2560x1440: pedir o original.
2. **Músicas**: `python3 ferramentas/sincronizar_musicas.py <slug>` copia só o que é novo do Drive sincronizado (`drive_musicas_mac`/`pasta_drive`) para `<pasta>/Musicas` e mostra os minutos disponíveis. Faixas que ficaram em ~/Downloads: `--extra ~/Downloads --desde-dias 3`. Jazz usa a pasta do Space Jazz Noir.
3. Gravações no SSD aparecem com atraso: conferir com `sleep 3`. Nunca apagar; mover lixo para `tmpm/`.
4. **Mixes**: `python3 ferramentas/montar_mixes.py "<pasta>" --minutos <duracao_min> --videos 3` (embaralha, não repete nome base no vídeo, para na duração alvo; gera `lista_videoN.txt` e `tracklist_videoN.txt`). Chill in Rio: `--so-portugues`. No segundo entre Classical Adagio e Ars Melancholia: `--evitar "<pasta do outro>"`. Snoopy: `--repetir`.
5. **Info**: `Videos finais/<nome>_video<N>_info.txt` e `_info.json` (título, descrição em inglês com 2 frases, tracklist e convite para inscrever, hashtags, tags, `publicar_em`). Sem travessões.
6. **Render e envio**: `CANAL=<slug> bash ferramentas/renderizar_videos.sh <nome> "1 2 3" <canto>` dentro da pasta do canal (EQ no canto oposto ao texto da arte). Uns 40 min por vídeo de 2h. No fim o `ferramentas/postar_youtube.py` passa pela trava, sobe e agenda sozinho; acompanhar `~/.capitao/youtube/registro.log`.
7. Upload só pelo `postar_youtube.py`. Nada de YouTube Studio no navegador. Mudanças de nome ou @ de canal: o Capitão faz.

## Padrão visual aprovado
2560x1440, 24 fps, fade in de 3s, EQ de 48 barras finas marfim com reflexo, pequeno, num canto.

## Script de render
`ferramentas/renderizar_videos.sh` (2560x1440, 24 fps, fade de 3 s, EQ marfim). Usa `Artes/<N>_loop.mp4` como fundo animado se existir. `POS_<N>=x:y` e `COR_<N>=0x...` ajustam posição e cor do EQ por vídeo.

## Regras do Capitão
Mínimo 2K. Sem travessões em textos. Prévias só se ele pedir mudança visual.