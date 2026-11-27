# Critérios para construir e manter o MorphoBr

> Documento de trabalho, para ir melhorando até chegarmos a uma visão consolidada.
> Começou em 2026-11-27 a partir de uma discussão sobre o que fazer quando as
> fontes discordam. As decisões marcadas como **proposta** ainda não foram
> tomadas; a pauta da reunião está em
> [#184](https://github.com/LR-POR/MorphoBr/issues/184).

## 1. O problema

Autores diferentes descrevem a morfologia do português com teorias diferentes.
Alguns são formais e chegam a regras precisas, inclusive de estados finitos.
Outros fazem uma descrição sem regras explícitas. Muitas vezes discordam sobre
a análise de um mesmo fenômeno. Por exemplo, sobre o feminino dos substantivos
(*professora*):

- é **flexão** para Câmara Jr. (1970) e Margotti & Margotti (2011, pp. 70–71),
  que é o modelo atual do MorphoBr (`professora professor+N+F+SG`);
- é **derivação**, um lexema distinto, para Sandmann (1991, pp. 21–22 e 36–40)
  e Villalva (2007, pp. 153–155).

Uma pergunta como "isto é flexão ou derivação?" não tem resposta empírica: a
resposta depende da teoria. Por isso o critério de decisão não pode ser
"escolher o autor certo". Ele tem de vir dos objetivos do próprio MorphoBr.

## 2. Dois tipos de pergunta

### 2.1 Perguntas de fato: a forma existe e como se escreve?

Exemplos: *pulo* é forma de *polir*? qual o plural dos nomes em *-z*? escreve-se
*cumprimentamo-nos*?

- Aqui não há teoria em jogo, só evidência.
- Vale a ordem de preferência das referências do README: Portal da Língua
  Portuguesa, VOLP, dicionários, Acordo Ortográfico de 1990. Gramáticas e
  livros de morfologia entram como evidência adicional, com a página.
- Quando as fontes de dados discordam, registram-se as duas formas, como na
  decisão de manter paradigmas completos
  ([#8](https://github.com/LR-POR/MorphoBr/issues/8)).
- A regularidade dos dados, sozinha, não é fonte. Uma mudança sem fonte forte
  fica num PR rascunho que diz qual referência falta.

### 2.2 Perguntas de modelagem: qual é o lema e quais traços entram?

Exemplos: o lema de *professora* ([#129](https://github.com/LR-POR/MorphoBr/issues/129)),
de *melhor* ([#88](https://github.com/LR-POR/MorphoBr/issues/88)), de *óculos*
([#83](https://github.com/LR-POR/MorphoBr/issues/83)); se o diminutivo é
`+DIM` do lema base ou lema próprio
([#164](https://github.com/LR-POR/MorphoBr/issues/164)).

Aqui os autores não estão errados: descrevem com teorias diferentes. Para
estas perguntas, **proposta** de três critérios, aplicados em ordem.

## 3. Critérios para as perguntas de modelagem (proposta)

### Critério 1: o lema é a entrada dos dicionários de referência

É um critério lexicográfico. Não depende de teoria, pode ser verificado e
corresponde ao que o usuário espera ao procurar uma palavra. Segue a ordem de
preferência do README, com o Portal em primeiro lugar.

Teste com seis palavras, numa consulta pontual em 2026-11-27:

| Palavra | Portal | Aulete | Priberam | Resultado |
|---|---|---|---|---|
| *melhor* | lema próprio | entrada própria | entrada própria | lema próprio |
| *pior* | lema próprio | entrada própria | entrada própria | lema próprio |
| *óculos* | lema próprio **e** plural de *óculo* | entrada própria (s.m.pl.) | entrada própria | lema próprio |
| *cabrita* | lema próprio **e** feminino do adj. *cabrito* | entrada própria | entrada própria | lema próprio |
| *férias* | só plural de *féria* | entrada própria (s.f.pl.) | entrada própria | as fontes divergem |
| *professora* | lema próprio | entrada própria | dentro de *professor* | maioria: lema próprio |

O Portal também dá *aluna* e *gata* como lemas próprios. Se adotarmos este
critério, o feminino dos substantivos passa a ser lema próprio, o que muda o
modelo atual. **Questão em aberto para a reunião.**

### Critério 2: não perder informação

Entre duas análises, prefere-se a que permite converter para a outra com um
script. Por exemplo, `professora professor+N+F+SG` permite gerar o lema
*professora* para quem segue Villalva ou Sandmann. O caminho inverso exige
conhecimento externo. Isso mantém o MorphoBr compatível com usuários que
adotam convenções diferentes, como o Bosque/UD e as gramáticas DELPH-IN e LFG,
sem tomar partido teórico.

Os critérios 1 e 2 podem entrar em conflito, como acontece no caso de
*professora*. Uma saída possível é dar o lema do dicionário e guardar a ligação
com o masculino num traço ou num mapeamento separado (a definir).

Quando as fontes divergem, uma opção é registrar as duas análises, como o
Portal faz com *óculos* (lema próprio e plural de *óculo*).

### Critério 3: regra para o que é regular e produtivo; lista para o resto

Os testes de Sandmann (1991, pp. 23–24) servem aqui: lacunas, obrigatoriedade e
produtividade automática. Eles não decidem se algo "é flexão". Decidem se vale
gerar por regra de estados finitos (`rules/`) ou listar no `.dict`, que é a
pergunta de engenharia que de fato temos
([#143](https://github.com/LR-POR/MorphoBr/issues/143)).

## 4. O papel dos autores

- Os **formais** (Villalva, e os trabalhos de morfologia de estados finitos)
  servem para estruturar as regras. Exemplo: *-zinho* se junta à palavra
  flexionada, e *-inho* ao radical, por isso *leõezinhos* e *pãezinhos*
  (Villalva 2007, pp. 122–124 e 163).
- Os **descritivos** servem como fonte de dados e de exceções.
- Nenhum autor decide sozinho uma questão de modelagem. As posições dos
  autores entram no registro da decisão (seção 6).

As referências estão no README, seção *Linguistic references*. As páginas que
já encontramos para cada issue estão comentadas nas próprias issues (#69, #83,
#88, #129, #159, #164, #173).

## 5. Corpus como fonte de palavras

**Proposta:** usar textos para encontrar palavras candidatas e medir
frequência. Uma palavra só entra no MorphoBr depois de conferida num dicionário
(seção 2.1).

### Fontes escolhidas

- o portal [Domínio Público](http://www.dominiopublico.gov.br/) do MEC;
- o [Projeto Gutenberg](https://www.gutenberg.org/), que tem livros em
  português;
- a [Wikipédia em português](https://pt.wikipedia.org/) (CC BY-SA).

### Pontos positivos

- **Atestação:** se uma palavra aparece num texto real, ela existe. Isso ajuda
  a achar palavras que faltam no MorphoBr e a decidir sobre estrangeirismos e
  neologismos que os vocabulários ainda não registram
  ([#148](https://github.com/LR-POR/MorphoBr/issues/148)). Villalva (2007, p. 26)
  trata da distinção entre palavras possíveis, existentes e atestadas (ainda a
  ler).
- **Frequência:** mostra quais formas importam mais, por exemplo para
  priorizar o que conferir à mão.
- **Licença:** como os textos são livres, podem ser processados em lote, ao
  contrário do Portal e do VOLP, que só admitem consultas pontuais.

### Pontos negativos

- **Ortografia antiga:** quase todo o domínio público é anterior às reformas de
  1943, 1971 e 1990 (*pharmacia*, *êle*, *idéia*). Cada forma precisa ser
  convertida ou marcada como grafia antiga, como já fazemos com as formas
  anteriores ao Acordo ([#93](https://github.com/LR-POR/MorphoBr/issues/93)).
- **Vocabulário:** sobretudo literário e antigo, muitas vezes europeu. Representa
  mal o português brasileiro atual. A Wikipédia compensa em parte.
- **Não é norma:** um texto mostra que a forma foi usada, não que está certa nem
  como se flexiona. Não substitui o Portal ou o VOLP para regras.
- **Ruído:** nomes próprios, estrangeirismos, erros de digitação e de OCR.
- **Classes fechadas:** o MorphoBr só cobre substantivos, adjetivos, verbos e
  advérbios. Artigos, preposições, pronomes e conjunções aparecem como
  "desconhecidos" e precisam ser filtrados.

### Experimento (em andamento)

Uma amostra de cada fonte, analisada com `flookup -i morphobr.bin` (release
v2026.11), para classificar as palavras sem análise em: classes fechadas,
nomes próprios, grafia antiga, estrangeirismos, erros e palavras que realmente
faltam. Resultados a acrescentar aqui.

## 6. Registro das decisões

Para não recomeçar a discussão quando aparecer um autor novo, cada decisão de
modelagem fica registrada com:

1. a pergunta e a issue;
2. as posições dos autores e dos dicionários, com as páginas;
3. o critério aplicado (seção 3);
4. a decisão e a data.

As decisões tomadas podem ser listadas aqui, numa seção própria, ou num
arquivo `docs/decisions.md` (a definir).

## 7. Questões em aberto

- Adotar o critério 1 mesmo quando ele muda o modelo atual (feminino dos
  substantivos, #129)?
- Como guardar a ligação entre lemas relacionados (*professora*/*professor*,
  *melhor*/*bom*) sem perder informação (critério 2)?
- Compatibilidade com o Bosque/UD: seguir a convenção deles quando ela diverge
  dos dicionários (#88)?
- O que fazer com as formas que só aparecem em corpus?
