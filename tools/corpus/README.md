# Cobertura do MorphoBr em corpus

Scripts para medir a cobertura do MorphoBr sobre amostras de texto e listar
as palavras sem análise. O método, as fontes escolhidas e o resultado da
primeira amostra estão em [`docs/principles.md`](../../docs/principles.md),
seção 5.

O corpus serve para achar palavras candidatas e medir frequência. Antes de
entrar no MorphoBr, toda palavra precisa ser conferida em dicionário
(`docs/principles.md`, seção 2.1).

## Requisitos

- `flookup` (foma) e um `morphobr.bin`: compilado com `compile.sh` ou baixado
  da [release](https://github.com/LR-POR/MorphoBr/releases);
- Python 3 com spaCy (`pip install spacy`). Não é preciso baixar nenhum modelo:
  só usamos o tokenizador e o `sentencizer`, que funcionam por regras. Os
  modelos treinados são evitados de propósito, porque vêm do Bosque/UD.

## Uso

```bash
# 1. amostras
python3 tools/corpus/fetch_wiki.py 100 /tmp/c/wiki.txt
python3 tools/corpus/fetch_gutenberg.py /tmp/c/gut 55752 55682 57001 40409 21406

# 2. limpeza, sentenças e tokens
python3 tools/corpus/prepare.py wiki /tmp/c/wiki /tmp/c/wiki.txt
python3 tools/corpus/prepare.py gutenberg /tmp/c/gut /tmp/c/gut/*.txt

# 3. cobertura e palavras sem análise
FLOOKUP=~/foma/foma/build/flookup \
  python3 tools/corpus/coverage.py morphobr.bin /tmp/c/wiki.tokens.tsv /tmp/c/gut.tokens.tsv \
  --oov /tmp/c/oov.tsv
```

Para outros textos, use `prepare.py plain` (parágrafos separados por linha em
branco).

## Arquivos

| Arquivo | Função |
|---|---|
| `fetch_wiki.py` | artigos aleatórios da Wikipédia em português, pela API, com pausa entre requisições |
| `fetch_gutenberg.py` | livros do Projeto Gutenberg pelo espelho oficial; IDs em português em <https://gutendex.com/books/?languages=pt> |
| `prepare.py` | limpeza (`wiki`, `gutenberg`, `plain`), sentenças e tokens |
| `coverage.py` | cobertura e categorias das palavras sem análise |
| `closed_class.txt` | palavras de classe fechada, excluídas da contagem |
