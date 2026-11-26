#!/bin/bash
# Gera o léxico de radicais (LEXICON Verbs) para rules/verbs.lexc a partir de
# lexicon/verbs/<modelo>.tsv: um lema por linha; o nome do arquivo é o
# verbo-modelo e, em maiúsculas, o nome da classe de flexão no lexc
# (abafar.tsv -> ABAFAR). O radical é o lema sem a terminação da classe,
# registrada em rules/classes.tsv.
#
# Uso: tools/lexicon-to-lexc.sh > tmp/verbs.lexc

set -euo pipefail
cd "$(dirname "$0")/.."

cat rules/verbs.lexc
echo
echo "LEXICON Verbs"
for f in lexicon/verbs/*.tsv; do
    model=$(basename "$f" .tsv)
    ending=$(awk -F'\t' -v m="$model" '!/^#/ && $1 == m {print $2}' rules/classes.tsv)
    if [ -z "$ending" ]; then
        echo "classe $model não está em rules/classes.tsv" >&2
        exit 1
    fi
    class=$(echo "$model" | tr '[:lower:]' '[:upper:]')
    awk -v class="$class" -v ending="$ending" '
        /^[[:space:]]*$/ { next }
        substr($0, length($0) - length(ending) + 1) != ending {
            print "lema sem -" ending " em " FILENAME ": " $0 > "/dev/stderr"; exit 1
        }
        {
            stem = substr($0, 1, length($0) - length(ending))
            gsub(/[%!;:<>"#0 -]/, "%&", stem)
            print stem " " class " ;"
        }' "$f"
done
