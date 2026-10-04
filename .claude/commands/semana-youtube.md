---
description: Orquestra a semana de vídeos de todos os canais (ou dos canais listados), em paralelo
argument-hint: "[canais separados por espaço, ex: chill-in-rio ars-melancholia] (vazio = todos)"
---
Você é o diretor da semana de YouTube do Capitão. Canais pedidos: $ARGUMENTS (vazio = todos de `canais/canais.json`).

1. Leia `canais/canais.json` e a data (`TZ=America/Campo_Grande date '+%F %A'`). Liste as publicações de segunda a domingo desta semana por canal, com dia e horário.
2. Confira o que já existe em cada pasta de canal (`Videos finais/`, `Artes/`) e em `vice-report/pacotes/` para não refazer nada. Se faltarem artes de um canal de música, peça ao Capitão numa única mensagem para todos os canais e siga com o resto.
3. Dispare em paralelo, numa única mensagem com várias chamadas da ferramenta Agent:
   * um `produtor-musica` por canal de música que tem artes, com o slug do canal e as datas da semana;
   * um `vice-report-video-longo` por vídeo longo do Vice Report BR desta semana que ainda não tem pacote, com a data de publicação.
   Se algum canal estiver com `observacoes` de relançamento ou sem `analise.md` de thumbs, dispare também um `estrategista-youtube` para ele.
4. Quando voltarem, rode um `revisor-youtube` com todos os vídeos e pacotes prontos.
5. Envio: os canais de música sobem e agendam sozinhos pelo `ferramentas/postar_youtube.py` logo depois do render (trava automática incluída). Se algum vídeo ficou pendente, rode `/postar`. O Vice Report BR não sobe sozinho: o Capitão envia.
6. Responda com uma tabela: canal | vídeo | publica em | status (pronto, falta render no Mac, falta arte, reprovado) | próximo passo. Sem travessões.
