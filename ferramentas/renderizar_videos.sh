#!/bin/bash
# Renderiza os videos de um canal de musica no padrao aprovado:
# 2560x1440, 24 fps, fade in de 3 s, EQ de 48 barras finas marfim com reflexo num canto.
#
# Uso (dentro da pasta do canal, com Artes/1.png.. e lista_video1.txt..):
#   bash renderizar_videos.sh <nome_saida> [videos] [canto]
#   nome_saida: ex. ars_melancholia   videos: ex. "1 2 3" (padrao)
#   canto: bl (baixo esq.), br (baixo dir., padrao), tl, tr. Use o canto oposto ao texto da arte.
#   CANAL=<slug> (ex. ars-melancholia) sobe e agenda no YouTube assim que termina.
#   POS_1, POS_2... e COR_1, COR_2... no ambiente sobrescrevem posicao (x:y) e cor por video.
#
# No Mac usa h264_videotoolbox; em outros sistemas cai para libx264.
set -euo pipefail
FERRAMENTAS="$(cd "$(dirname "$0")" && pwd)"
cd "${PASTA:-.}"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
command -v ffmpeg >/dev/null || { command -v brew >/dev/null && brew install ffmpeg; }

NOME="${1:?informe o nome de saida, ex: ars_melancholia}"
VIDEOS="${2:-1 2 3}"
CANTO="${3:-br}"
case "$CANTO" in
  bl) POS_PADRAO="150:1300" ;;
  br) POS_PADRAO="1980:1300" ;;
  tl) POS_PADRAO="150:120" ;;
  tr) POS_PADRAO="1980:120" ;;
  *) echo "canto invalido: $CANTO" >&2; exit 1 ;;
esac

if ffmpeg -hide_banner -encoders 2>/dev/null | grep -q h264_videotoolbox; then
  VCODEC=(-c:v h264_videotoolbox -b:v 8M)
else
  VCODEC=(-c:v libx264 -preset medium -crf 20)
fi

mkdir -p "Videos finais"
for v in $VIDEOS; do
  out="Videos finais/${NOME}_video$v.mp4"
  [ -s "$out" ] && { echo "ja existe: $out"; continue; }
  arte=""
  for ext in png jpg jpeg; do [ -f "Artes/$v.$ext" ] && arte="Artes/$v.$ext" && break; done
  [ -n "$arte" ] || { echo "falta Artes/$v.png" >&2; exit 1; }
  [ -f "lista_video$v.txt" ] || { echo "falta lista_video$v.txt" >&2; exit 1; }
  pv="POS_$v"; cv="COR_$v"
  pos="${!pv:-$POS_PADRAO}"; col="${!cv:-0xF3E6C6}"
  audio="${TMPDIR:-/tmp}/render_${NOME}_${v}_$$.m4a"
  echo "== video $v: juntando audio"
  ffmpeg -y -loglevel error -f concat -safe 0 -i "lista_video$v.txt" -c:a aac -b:a 192k -ar 48000 "$audio"
  echo "== video $v: renderizando"
  ffmpeg -y -loglevel error -stats -loop 1 -framerate 24 -i "$arte" -i "$audio" -filter_complex \
"[0:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,format=yuv420p[bg];\
[1:a]aformat=channel_layouts=mono,highpass=f=50,lowpass=f=9000,showfreqs=s=48x44:mode=bar:ascale=log:fscale=log:win_size=2048:averaging=3:overlap=0.75:colors=$col,\
format=rgba,scale=432:44:flags=neighbor,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(gte(mod(X,9),3),0,alpha(X,Y)*0.8)',split[t][r];\
[r]vflip,colorchannelmixer=aa=0.25,crop=432:16:0:0[rf];[t][rf]vstack,fps=24[w];\
[bg][w]overlay=$pos:shortest=1,fade=t=in:st=0:d=3[v]" \
    -map "[v]" -map 1:a "${VCODEC[@]}" -r 24 -c:a copy -shortest -movflags +faststart "$out.tmp.mp4"
  mv "$out.tmp.mp4" "$out"
  rm -f "$audio"
  echo "pronto: $out"
done
echo PRONTO
# Envio automatico: com CANAL=<slug> no ambiente, sobe e agenda logo depois do render.
if [ -n "${CANAL:-}" ]; then
  python3 "$FERRAMENTAS/postar_youtube.py" enviar . --canal "$CANAL"
fi
