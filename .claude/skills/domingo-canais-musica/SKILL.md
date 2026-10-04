---
name: "domingo-canais-musica"
description: "Produção semanal (domingo) dos vídeos dos canais de música do Capitão: ele manda as fotos, Claude sincroniza músicas no SSD, renderiza 2K com fade e EQ no Mac, sobe e agenda no YouTube."
---

# Domingo: vídeos dos canais de música

O Capitão só manda as fotos e diz o canal. Claude faz o resto sem pedir nada além do necessário. Siga exatamente este caminho; os outros já falharam.

## Canais
| Canal | Estilo | Duração | Horário (Campo Grande) |
|---|---|---|---|
| Chill in Rio | bossa nova (só faixas com nome em português) | padrão do canal | padrão do canal |
| Space Jazz Noir | jazz | 2h | 18h |
| MindForge Studio | ambient | 2h15 a 2h30 | 8h |
| Classical Adagio Music (@ClassicalAdagioMusic) | neoclássico relax acadêmico | 2h | 18h30 |
| Ars Melancholia | neoclássico sombrio | 2h | 19h |

Publicação seg, qua, sex. Classical Adagio e Ars Melancholia compartilham faixas (ordem diferente, nunca a mesma faixa nos dois na mesma semana). Primeiro vídeo de canal novo: rascunho privado até o Capitão aprovar.

## Não tente (já falhou)
- Baixar de Drive ou Canva pelo Bash da nuvem ou pelo device_bash: rede bloqueada.
- Renderizar no device_bash: VM lenta e mata processos a cada chamada.
- Filesystem MCP do Mac: erro de schema.

## Fluxo
1. **Acesso** (no início, um pedido só): device_request_folder_access para o SSD externo (`volume_ssd` em ~/.capitao/local.json) e a pasta do Google Drive para computador (`drive_musicas_mac` de ~/.capitao/local.json). Se o Drive para computador não estiver instalado, usar ~/Downloads e baixar a pasta Musicas novas pelo Claude in Chrome (Drive > ⋮ > Baixar), pedindo uma única confirmação para todos os downloads da sessão.
2. **Fotos**: vêm anexadas no chat ou em ~/Downloads. Salvar em `01 CANAIS/<CANAL>/Artes/1.png, 2.png, 3.png`.
3. **Músicas**: copiar do Drive sincronizado para `01 CANAIS/<CANAL>/Musicas/` só o que for novo (`rsync -a --ignore-existing`). Jazz usa a pasta do Space Jazz Noir.
4. Gravações no SSD (fuse) aparecem com atraso: conferir com `sleep 3`. `rm` não é permitido; mover lixo para `tmpm/`.
5. **Mixes** (python, scripts em ~/w): embaralhar, não repetir nome base no vídeo (ignorar sufixos " (1)"), parar na duração alvo. Gerar `lista_video{1,2,3}.txt` (`file 'Musicas/<nome>.mp3'`) e tracklist H:MM:SS.
6. **Info**: `Videos finais/<canal>_video{v}_info.txt` com título, descrição em inglês (2 frases + tracklist + convite para inscrever), hashtags e tags. Sem travessões.
7. **Render no Mac nativo**: script abaixo em `<CANAL>/RENDERIZAR_VIDEOS.command` (ajustar NOME, pos e col; EQ no canto oposto ao texto da arte). Abrir via computer use: Finder (full) + Terminal (click), request_full_control, app_release antes das ferramentas de tela, Finder > Ir > Ir para Pasta, digitar caminho do .command, Enter, duplo clique. Dois monitores: Tela Retina Integrada e ARZOPA (switch_display). ~40 min por vídeo de 2h.
8. send_later em ~45 min para checar `Videos finais/` e subir.
9. **Upload**: YouTube Studio no Claude in Chrome (avatar > Mudar de conta), preencher do info.txt, agendar no horário do canal. Mudanças de nome ou @ de canal: o Capitão faz.

## Padrão visual aprovado
2560x1440, 24 fps, fade in de 3s, EQ de 48 barras finas marfim com reflexo, pequeno, num canto.

## Script de render
```bash
#!/bin/bash
cd "$(dirname "$0")" || exit 1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
command -v ffmpeg >/dev/null || brew install ffmpeg
NOME=ars_melancholia
pos=( "" "300:1090" "1980:1230" "150:1230" ); col=( "" "0xF2E2B8" "0xF3E6C6" "0xF3E6C6" )
for v in 1 2 3; do
  out="Videos finais/${NOME}_video$v.mp4"
  [ -s "$out" ] && continue
  ffmpeg -y -loglevel error -f concat -safe 0 -i lista_video$v.txt -c:a aac -b:a 192k -ar 48000 /tmp/a$v.m4a
  ffmpeg -y -loglevel error -stats -loop 1 -framerate 24 -i "Artes/$v.png" -i /tmp/a$v.m4a -filter_complex "[0:v]scale=2560:1440,format=yuv420p[bg];[1:a]aformat=channel_layouts=mono,highpass=f=50,lowpass=f=9000,showfreqs=s=48x44:mode=bar:ascale=log:fscale=log:win_size=2048:averaging=3:overlap=0.75:colors=${col[$v]},format=rgba,scale=432:44:flags=neighbor,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(gte(mod(X,9),3),0,alpha(X,Y)*0.8)',split[t][r];[r]vflip,colorchannelmixer=aa=0.25,crop=432:16:0:0[rf];[t][rf]vstack,fps=24[w];[bg][w]overlay=${pos[$v]}:shortest=1,fade=t=in:st=0:d=3[v]" -map "[v]" -map 1:a -c:v h264_videotoolbox -b:v 8M -r 24 -c:a copy -shortest -movflags +faststart "$out.tmp.mp4" && mv "$out.tmp.mp4" "$out"
done
echo PRONTO; read
```

## Regras do Capitão
Mínimo 2K. Sem travessões em textos. Prévias só se ele pedir mudança visual.