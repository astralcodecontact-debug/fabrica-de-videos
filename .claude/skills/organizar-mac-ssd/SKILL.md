---
name: "organizar-mac-ssd"
description: "Liberar espaço no Mac do Capitão: achar o que pesa, mover para o SSD externo com conferência arquivo por arquivo, organizar Downloads em pastas e apagar só duplicados exatos."
---

# Organizar o Mac e mandar para o SSD

Use quando o Capitão disser que o HD está cheio, pedir para organizar Downloads ou pastas, ou para mandar arquivos para o SSD.

Regra fixa de texto: nunca usar travessão nem hífen como pontuação em nada entregue ao Capitão.

## Acesso
* Ferramentas mcp__remote-devices__ (device_bash, device_request_folder_access, device_request_delete_permission).
* Peça numa única vez as pastas: ~/Desktop, ~/Documents, ~/Downloads, ~/Movies, ~/Music, ~/Pictures (e outras da home se fizer sentido) e /Volumes (onde aparece o SSD externo).
* Apagar vem desligado: peça device_request_delete_permission uma vez para as pastas raiz envolvidas (Movies, Downloads, Documents, /Volumes) explicando que só apaga depois de copiar e conferir.
* No device_bash as pastas ficam em $HOME/mnt/<nome>; o SSD em $HOME/mnt/Volumes/<nome do SSD em volume_ssd>. Pastas ocultas (com ponto) no SSD não funcionam bem; use $HOME/mover dentro da VM para listas e scripts.

## 1. Diagnóstico
* `du -sh` em cada pasta e depois descendo nas maiores. O vilão costuma ser o CapCut: `Movies/CapCut/User Data/Cache/SmartCrop` (renderizações do Reenquadrar automático, vários GB cada) e vídeos exportados soltos em Movies/CapCut.
* Mostre ao Capitão o que achou e pergunte (AskUserQuestion) se o cache vai para o SSD ou é apagado. Padrão recomendado: mover para o SSD.
* Antes de mexer em pastas, confira se algum agente agendado usa o caminho (list_triggers). `Documents/Vice Report BR` é usado pelo agente diário: NÃO mover.

## 2. Estrutura do SSD externo
```
01 CANAIS/
  CHILL IN RIO (Bossa Nova)/  Musicas, Videos finais, Cache CapCut
  MINDFORGE/                  Musicas, Videos finais, Cache CapCut
  FERNANDO BELMONTE/          Musicas, Cache CapCut
  THE JAZZ CLUB/              Musicas
  VICE REPORT BR (GTA 6)/     Videos finais, Videos brutos, Pacotes de imagens
02 CAPCUT OUTROS/   (vídeos sem canal claro)
03 INSTALADORES/    (.dmg e afins)
```
Classificação por nome: chill in rio, sunny in rio, brazil relax, vintage brasil = Chill in Rio; mindforge, mind forge, 0906 = MindForge; fernando belmonte, Ficou o Samba = Fernando Belmonte; videoplayback*.webm, zips GTAVI e vr_* = Vice Report. Na dúvida, 02 CAPCUT OUTROS e avise. Se aparecer canal novo (ex: The Reading Room), crie a pasta dele no mesmo padrão. Pastas temporárias vazias do CapCut (`.__capcut_export_temp_folder_*`) podem ser removidas.

## 3. Mover com segurança
* Script no Mac: `~/Documents/Vice Report BR/_ferramentas/ssd/mover_ssd.sh`. Copie para $HOME/mover.
* Monte `lista.txt` com linhas `origem|pasta destino`, ordenadas do menor para o maior arquivo.
* Rode `bash $HOME/mover/mover_ssd.sh $HOME/mover/lista.txt 165` repetidas vezes até aparecer FIM. Ele copia com rsync retomável, confere tamanho e os primeiros e últimos 256 MB com cmp, e só então apaga a origem. Mensagens de SIGTERM do rsync no fim de cada lote são normais.
* A escrita no SSD pela VM é lenta (~20 MB/s, ~3 GB por chamada). Avise o Capitão do tempo estimado antes de começar (ex: 86 GB ≈ 1 hora).
* Processos em segundo plano morrem ao fim de cada chamada do device_bash: tudo em primeiro plano, lotes de até ~170 s.

## 4. Organizar Downloads (no próprio Mac)
* Apague só duplicados EXATOS: `X (1).ext` igual byte a byte a `X.ext` (cmp), e pastas extraídas repetidas (`X 2`, `X 3`) iguais pelo `diff -rq`. Nunca apague algo só por parecer repetido.
* Pastas: 01 Vice Report BR (GTA 6) [Narracoes ElevenLabs, Videos, Imagens e pacotes, Artes do perfil], 02 MindForge, 03 Chill in Rio, 04 Alfredo Caopany, 05 Faculdade, 06 Imagens IA (Higgsfield, arquivos hf_*), 07 Fotos e prints (IMG_*, WhatsApp, jpgs com nome aleatório), 08 Musicas Suno (mp3/m4a soltos), 09 Outros e programas.
* Use `mv -n` (nunca sobrescrever). Arquivos pesados (webm, zips grandes, .dmg) vão para o SSD pela lista do passo 3.
* Novos downloads continuam caindo na raiz de Downloads (o fluxo do ElevenLabs depende disso).

## 5. Fechamento
* Meça de novo (`du -sh`) e informe quanto foi liberado, a estrutura final do SSD com tamanhos e o que não foi mexido.
* Lembretes ao Capitão: se uma pasta de exportação do CapCut mudou de lugar, escolher a nova no próximo export; o cache interno restante do CapCut se limpa em Configurações > Cache dentro do app; Fotos e Lightroom são bibliotecas e não se movem pela VM; iCloud e Google Drive não ficam visíveis daqui.
* Remova $HOME/mover no fim.