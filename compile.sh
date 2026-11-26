#!/bin/bash
# Compila os dicionários do MorphoBr num transdutor foma (morphobr.bin).
#
# Requer:
#  - python3, para converter os dicionários (tools/dict2stxt.py) e gerar os
#    diminutivos (tools/dim.py);
#  - foma com pilha dinâmica (https://github.com/mhulden/foma/pull/176)
#    ou com MAX_STACK aumentado em foma/int_stack.c. Para usar um foma
#    fora do PATH, defina FOMA, p.ex.: FOMA=~/foma/foma/build/foma ./compile.sh

set -euo pipefail

cd "$(dirname "$0")"

FOMA=${FOMA:-foma}
TMP=tmp

mkdir -p $TMP
rm -f $TMP/*.stxt

for d in nouns verbs clitics adjectives adverbs; do
    python3 -B tools/dict2stxt.py $d/*.dict > $TMP/$d.stxt
done

# léxico de radicais + paradigmas dos verbos gerados por regras (ver #143)
tools/lexicon-to-lexc.sh > $TMP/verbs.lexc

# diminutivos gerados por regras (rules/dim/ + lexicon/dim/, ver #149)
FOMA="$FOMA" python3 -B tools/dim.py generate > $TMP/dim.dict
python3 -B tools/dict2stxt.py $TMP/dim.dict > $TMP/dim.stxt

"$FOMA" -f compile.foma

rm $TMP/*.stxt $TMP/verbs.lexc $TMP/dim.dict
