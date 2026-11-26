#!/bin/bash
# Ordem canônica dos dicionários: por análise (lema primeiro) e depois
# por forma, comparando bytes (LC_ALL=C), sem linhas repetidas.
# Assim todas as entradas de um lema ficam juntas e os diffs só mostram
# mudanças reais.
#
# Uso: tools/canonicalize.sh          ordena os arquivos no lugar
#      tools/canonicalize.sh --check  só verifica; sai com erro se algum
#                                     arquivo não estiver na ordem canônica

set -euo pipefail
cd "$(dirname "$0")/.."
export LC_ALL=C

status=0
for f in {nouns,verbs,adjectives,adverbs,clitics}/*.dict; do
    if [ "${1:-}" = "--check" ]; then
        if ! sort -t$'\t' -k2,2 -k1,1 -u -c "$f" 2>/dev/null; then
            echo "fora da ordem canônica: $f"
            status=1
        fi
    else
        sort -t$'\t' -k2,2 -k1,1 -u -o "$f" "$f"
    fi
done
exit $status
