#!/bin/bash
# Compila os dicionários do MorphoBr num transdutor foma (morphobr.bin).
#
# Requer:
#  - stack, para compilar o conversor em code/;
#  - foma com pilha dinâmica (https://github.com/mhulden/foma/pull/176)
#    ou com MAX_STACK aumentado em foma/int_stack.c. Para usar um foma
#    fora do PATH, defina FOMA, p.ex.: FOMA=~/foma/foma/build/foma ./compile.sh

set -euo pipefail

cd "$(dirname "$0")"

FOMA=${FOMA:-foma}
TMP=tmp

(cd code && stack build --silent)
EXE="$(cd code && stack path --local-install-root)/bin/code-exe"

mkdir -p $TMP
rm -f $TMP/*.stxt

for d in nouns verbs clitics adjectives adverbs; do
    for f in $d/*.dict; do
        "$EXE" -m "$f" | tr -d '\r'
    done > $TMP/$d.stxt
done

# léxico de radicais + paradigmas dos verbos gerados por regras (ver #143)
tools/lexicon-to-lexc.sh > $TMP/verbs.lexc

"$FOMA" -f compile.foma

rm $TMP/*.stxt $TMP/verbs.lexc
