---
name: "vice-report-carrossel"
description: "Criar carrossel de Instagram do Vice Report BR (notícia, comparativo GTA 5 x GTA 6 ou opinião fora da caixinha) com fotos 2K/4K que combinam com cada slide, enquadramento manual e legenda."
---

# Carrossel do Vice Report BR

Use quando o Capitão pedir um carrossel (com ou sem imagem de capa enviada por ele) ou a legenda de um carrossel.

Regra fixa de texto: nunca usar travessão nem hífen como pontuação em nada entregue ao Capitão.

Regra da data de lançamento: NÃO repetir em todo post que o GTA 6 sai em 19 de novembro. Nem no último slide (sem "FALTAM N DIAS" e sem "até 19 de novembro") nem na legenda. A data só entra quando o próprio assunto do post for o lançamento, a pré venda ou a contagem regressiva (a contagem já tem o post próprio de countdown).

Visual: o modelo roxo e rosa do `_modelo` é o aprovado. Não trocar por outros estilos (The Verge e PlayStation foram testados e o original ficou melhor), a não ser que o Capitão peça.

## Arquivos no Mac
* Modelo: `Documents/Vice Report BR/Carrosseis/_modelo/` (carrossel.html, carrossel.js, exemplo_slides.json, fonts/).
* Referência aprovada: `Carrosseis/04 Detalhes que passaram batido/` (slides.json e slides).
* Fotos: `Documents/Vice Report BR/Imagens GTA 6/`: 01 a 10 fotos oficiais 4K; `11 Artes e Extras` artes oficiais em vários formatos (_portrait 2160x3840 é ótima para 4:5); `13 Extended Look 4K` 48 frames 4K de vídeo. NUNCA use `Frames dos Trailers` (Full HD, reprovada). GTA 5 em `Imagens GTA 5/`.
* Log: `Carrosseis/_fotos_usadas.txt`.

## Passo a passo
1. **Tema e fatos**: 5 ou 6 fatos reais confirmados em fonte primária; rumor só marcado como RUMOR. Tipos: notícia (seg e qua), comparativo GTA 5 x GTA 6 (sex, sub no formato "GTA 5: ... | GTA 6: ..."), fora da caixinha (dom, os dois lados + nossa opinião marcada como opinião). Confira os carrosséis anteriores para não repetir os mesmos fatos.
2. **Textos** (formato do exemplo_slides.json): capa com `k` (CONFIRMADO, NOVIDADE, RUMOR, COMPARATIVO, OPINIÃO), `t` curto com *destaques* entre asteriscos, `sub` com promessa honesta, `fs: 112`. Slides de fato com `num`, `t` até 8 palavras, `sub` 1 frase, `src`. O fato mais forte por último. Último slide com `k` tipo "SUA OPINIÃO" ou "E AÍ?", pergunta para comentar e chamada para seguir @vicereportbr, sem data de lançamento nem contagem (ver regra acima). Todo slide com `"pal": "roxo", "sat": "1.05", "con": "1.02"` (cor natural: o Capitão não quer foto saturada demais; nunca passar de 1.1); sem os campos font e mode.
3. **Fotos com qualidade boa e que fazem sentido com o texto**: para cada slide pense no que o texto diz e procure a cena que mostra isso (preço = capa oficial; personagem = aquele personagem; mapa = vista aérea; hype = multidão; carona = gente dentro do carro). Prefira sempre screenshots oficiais (pastas 01 a 11). Use frame do `13 Extended Look 4K` só quando nenhuma foto oficial mostrar o assunto, e nunca frame escuro, borrado ou com faixa preta. Monte folha de contato com Pillow e olhe antes de escolher. Não repita foto usada nos últimos 10 carrosséis. Sem interface do jogo no recorte. Se faltar foto, baixe oficial 2K/4K (rockstargames.com/VI/media, gtaboom 4K) e confira a resolução (mínimo 2560 px no lado maior).
4. **Enquadramento manual**: recorte 4:5 com Pillow (largura = altura x 0,8), com o assunto inteiro na METADE DE CIMA (a de baixo leva texto e degradê); rostos nunca cortados, nem na borda; duplas aparecem inteiras. Redimensione para 1296x1620 com LANCZOS + UnsharpMask (raio 1, 40%, limiar 2), salve como `img/kNN.jpg` e use `"fx": 0.5`. Olhe a folha dos recortes e refaça o que cortar rosto ou deixar o assunto embaixo do texto. Se o Capitão mandar a capa, use a imagem dele no slide 1.
5. **Renderizar** no container: `npm i playwright` e `SCALE=2 node carrossel.js slides.json /mnt/user-data/outputs/carrossel`. Confira cada slide com Read (texto legível, rosto livre, foto nítida, cor natural e coerente com o texto). Refaça o que falhar.
6. **Salvar**: pasta `Carrosseis/<NN tema curto>/` (NN = próximo número) com slides, slides.json, img/ e legenda.txt; acrescente "<pasta> | <arquivo original>" no _fotos_usadas.txt. Envie os slides com SendUserFile.
7. **Legenda** (quando pedir ou junto da entrega): primeira linha repetindo o gancho da capa, resumo curto, pergunta para comentar, chamada para seguir @vicereportbr e no máximo 5 hashtags (limite do Instagram). Sem data de lançamento, a não ser que o post seja sobre ela. Mande pronta para copiar.