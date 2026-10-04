---
name: "vice-report-thumbnail"
description: "Criar thumbnails de YouTube do Vice Report BR no estilo MrBeast com texto em neon de Vice City, sempre em duas versões com o mesmo texto e fotos oficiais 4K diferentes, recorte limpo."
---

# Thumbnail de YouTube do Vice Report BR

Use quando o Capitão pedir thumbnail (ou capa de vídeo longo) para o Vice Report BR.

Regra fixa de texto: nunca usar travessão nem hífen como pontuação em nada entregue ao Capitão.

## Entrega padrão
* SEMPRE duas versões com o MESMO texto e fotos DIFERENTES (personagem e fundo diferentes): uma com personagem à esquerda e texto à direita, outra invertida.
* Texto curto (1 a 4 palavras). Se o Capitão mandar um texto longo, sugira a forma curta (ex.: "NOVIDADES DE GTA 6"), mas faça o que ele pediu.

## Identidade do YouTube (separada do Instagram)
* Não segue o visual dos carrosséis. Estrutura MrBeast: personagem GRANDE recortado com contorno branco uniforme e sombra suave; fundo da própria foto do jogo, mais claro e desfocado, com leve tom roxo e rosa (`"tint":"vice"`).
* Texto padrão NEON (escolhido pelo Capitão): fonte Big Shoulders Display 900, SEM borda preta. Linha 1 em neon rosa (letra rosa clarinho com brilho rosa e magenta); linha 2 branca com sombra suave e a palavra de destaque (ex.: GTA 6) em neon ciano. Um degradê escuro roxo atrás do lado do texto garante a leitura.
* Rejeitados pelo Capitão: Lilita One e fontes arredondadas (cara de IA), contorno preto grosso nas letras.
* Sem logo grande. Canto inferior direito livre (duração do vídeo). Cor natural na foto do personagem.

## Fotos
* Só imagens oficiais 4K de `Documents/Vice Report BR/Imagens GTA 6/`. Nunca `Frames dos Trailers`.
* VARIAR: leia `Thumbnails/_fotos_usadas.txt` e `Carrosseis/_fotos_usadas.txt` e não repita foto recente. Explore Coadjuvantes (Boobie Ike, Real Dimez, Raul Bautista, Cal Hampton, DreQuan, Brian Heder), Vice City, Ambrosia, Port Gellhorn, Grassrivers, 11 Artes e Extras.
* Potencial viral: rosto olhando para a câmera, expressão forte, algo icônico ou bizarro.
* Para recorte, só fotos com personagem bem iluminado e separado do fundo. Foto escura ou com fumaça ou neon atrás recorta mal: troque de foto.
* Nunca gerar nem editar por IA rosto, expressão ou aparência de personagens da Rockstar. Se a ideia pede isso, ache uma foto oficial que já tenha esse visual.

## Ferramentas (no Mac em `Documents/Vice Report BR/_ferramentas/thumbnail/`)
* Traga `cut.py`, `compose.py` e `txt.js` para o container com device_stage_files. Instale: `pip install --break-system-packages "rembg[cpu]" scipy` e, em /tmp/c04, `npm i playwright @fontsource/big-shoulders-display` (o txt.js procura os módulos em /tmp/c04/node_modules; ajuste o caminho se preciso).
* `python3 cut.py <imagem> <nome> isnet-general-use`: recorta numa cópia de 1600 px e aplica a máscara na foto 4K. Os modelos birefnet e bria estouram a memória do container.
* `python3 compose.py '<json>'`: base em 2560x1440 com limpeza de franja, remoção de ilhas, preenchimento de buracos pequenos, contorno branco uniforme e sombra. Campos: bg, cut, crop [x0,y0,x1,y1], h, x, y, bgx, bgy, bgzoom, blur, bright, tint ("vice").
* `node txt.js <base.jpg> <saida.png> <dir|esq> "<linha 1>" "<linha 2 com *destaque*>" [tamanho1] [tamanho2]`: aplica o texto neon com o degradê escuro do lado certo.

## Passo a passo
1. Defina o texto.
2. Escolha 2 personagens e 2 fundos diferentes fora do registro. Monte folha de contato e olhe antes de decidir.
3. Recorte e confira sobre fundo verde. Se vier transparente, fantasma ou com pedaços do fundo, troque de foto (não remendar com retângulos).
4. Monte com compose.py usando tint vice. Nunca deixe aparecer o corte reto do recorte: use crop largo e deixe o corpo sair pela borda.
5. Ponha o texto com txt.js. Confira com Read em tamanho real e com zoom na borda do recorte: contorno liso, rosto inteiro, texto dentro do quadro e sem tampar rosto.
6. Teste do polegar: reduza para 200x113 e veja se ainda lê.
7. Salve em `Thumbnails/<tema>/versao_1_<personagem>.jpg` e `versao_2_<personagem>.jpg`, registre as fotos em `Thumbnails/_fotos_usadas.txt` e envie as duas com SendUserFile.
8. Diga qual aposta e por quê, sugira subir as duas no Test & Compare do YouTube e aponte qualquer informação do vídeo sem fonte confirmada.