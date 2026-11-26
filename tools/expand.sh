#!/bin/bash
# Escreve na saída padrão a lista full-form completa (forma<TAB>análise):
# os pares dos arquivos .dict mais os gerados pelas regras (rules/ +
# lexicon/, ver #143), em ordem canônica e sem repetição.
#
# Uso: tools/expand.sh [classe...]   (padrão: nouns verbs clitics adjectives adverbs)
# Variável FOMA: caminho do foma (padrão: foma no PATH).

set -euo pipefail
cd "$(dirname "$0")/.."
FOMA=${FOMA:-foma}
classes=${*:-nouns verbs clitics adjectives adverbs}

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

{
    for c in $classes; do
        cat "$c"/*.dict
        if [ "$c" = verbs ] && ls lexicon/verbs/*.tsv > /dev/null 2>&1; then
            tools/lexicon-to-lexc.sh > "$tmp/verbs.lexc"
            printf 'read lexc %s/verbs.lexc\ndefine Lex ;\nsource rules/orthography.foma\nregex Lex .o. Orthography ;\nprint pairs > %s/pairs.txt\n' \
                "$tmp" "$tmp" > "$tmp/gen.foma"
            "$FOMA" -f "$tmp/gen.foma" > "$tmp/foma.log" 2>&1 || { cat "$tmp/foma.log" >&2; exit 1; }
            awk -F'\t' '{print $2 "\t" $1}' "$tmp/pairs.txt"
        fi
    done
} | LC_ALL=C sort -t$'\t' -k2,2 -k1,1 -u
