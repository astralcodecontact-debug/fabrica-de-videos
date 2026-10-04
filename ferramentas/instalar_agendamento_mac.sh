#!/bin/bash
# Instala no macOS (launchd) uma rodada diaria de reserva do envio ao YouTube, as 3h.
# Ela sobe o que ficou para tras (cota da API esgotada, Mac desligado no fim do render).
# Desinstalar: launchctl unload ~/Library/LaunchAgents/com.capitao.postar-youtube.plist && rm esse arquivo
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST=~/Library/LaunchAgents/com.capitao.postar-youtube.plist
PY="$(command -v python3)"
mkdir -p ~/Library/LaunchAgents ~/.capitao/youtube
cat > "$PLIST" <<P
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.capitao.postar-youtube</string>
  <key>ProgramArguments</key><array>
    <string>$PY</string><string>$DIR/postar_youtube.py</string><string>enviar-todos</string>
  </array>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string></dict>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>3</integer><key>Minute</key><integer>7</integer></dict>
  <key>StandardOutPath</key><string>$HOME/.capitao/youtube/launchd.log</string>
  <key>StandardErrorPath</key><string>$HOME/.capitao/youtube/launchd.log</string>
</dict></plist>
P
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "Agendado: todo dia as 3h07 o Mac sobe o que estiver pendente. Log em ~/.capitao/youtube/registro.log"
echo "Para o Mac acordar sozinho: sudo pmset repeat wakeorpoweron MTWRFSU 03:00:00"
