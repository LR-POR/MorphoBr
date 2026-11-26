#!/bin/bash
# Gera o léxico de radicais (LEXICON Verbs) para rules/verbs.lexc a partir de
# lexicon/verbs/<modelo>.tsv: um lema por linha; o nome do arquivo é o
# verbo-modelo e, em maiúsculas, o nome da classe de flexão no lexc
# (abafar.tsv -> ABAFAR). O radical é o lema sem a terminação -ar.
#
# Uso: tools/lexicon-to-lexc.sh > tmp/verbs.lexc

set -euo pipefail
cd "$(dirname "$0")/.."

cat rules/verbs.lexc
echo
echo "LEXICON Verbs"
for f in lexicon/verbs/*.tsv; do
    class=$(basename "$f" .tsv | tr '[:lower:]' '[:upper:]')
    awk -v class="$class" '
        /^[[:space:]]*$/ { next }
        $0 !~ /ar$/ { print "lema sem -ar em " FILENAME ": " $0 > "/dev/stderr"; exit 1 }
        {
            stem = substr($0, 1, length($0) - 2)
            gsub(/[%!;:<>"#0 -]/, "%&", stem)
            print stem " " class " ;"
        }' "$f"
done
