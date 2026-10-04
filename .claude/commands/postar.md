---
description: Sobe e agenda no YouTube tudo o que estiver pronto nos canais de música
argument-hint: "[canal] (vazio = todos) [--simular]"
---
Rode no Mac, a partir da raiz do repositório:
* com canal: `python3 ferramentas/postar_youtube.py enviar "<raiz_canais_mac>/<pasta do canal>" --canal <canal>` (pegue a pasta em canais/canais.json)
* sem canal: `python3 ferramentas/postar_youtube.py enviar-todos`
Argumentos: "$ARGUMENTS" (repasse --simular se vier). Depois mostre as linhas novas de `~/.capitao/youtube/registro.log` numa tabela: canal | vídeo | resultado (link, reprovado e motivo, cota, não autorizado). Código de saída 3 = cota diária da API acabou; diga que o resto sobe sozinho às 3h07 se o agendamento estiver instalado.
