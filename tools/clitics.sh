#!/bin/bash
# Escreve na saída padrão os pares forma<TAB>análise das formas com clíticos
# geradas pelas regras (rules/clitics.foma, ver #165) para os lemas de
# lexicon/clitics/verbs.tsv (ou do arquivo dado), a partir dos verbos
# regulares (rules/ + lexicon/verbs/) e irregulares (verbs/*.dict).
#
# Uso: tools/clitics.sh [LEMAS]
# Variável FOMA: caminho do foma (padrão: foma no PATH).

set -euo pipefail
cd "$(dirname "$0")/.."
FOMA=${FOMA:-foma}
lemmas=$(cd "$(dirname "${1:-lexicon/clitics/verbs.tsv}")" && pwd)/$(basename "${1:-lexicon/clitics/verbs.tsv}")

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

tools/lexicon-to-lexc.sh > "$tmp/verbs.lexc"
python3 -B tools/dict2stxt.py verbs/*.dict > "$tmp/verbs.stxt"
cat > "$tmp/gen.foma" <<FOMA
read lexc $tmp/verbs.lexc
define verbLex ;
source rules/orthography.foma
define VerbRules verbLex .o. Orthography ;
read spaced-text $tmp/verbs.stxt
define verbs ;
define VerbAn VerbRules | verbs.i ;
read text $lemmas
define CliticLemmas ;
source rules/clitics.foma
regex Clitic ;
print pairs > $tmp/pairs.txt
FOMA
"$FOMA" -f "$tmp/gen.foma" > "$tmp/foma.log" 2>&1 || { cat "$tmp/foma.log" >&2; exit 1; }
grep -q '^Error\|^\*\*\*' "$tmp/foma.log" && { cat "$tmp/foma.log" >&2; exit 1; }
awk -F'\t' '{print $2 "\t" $1}' "$tmp/pairs.txt"
