set -x

tmp1=$(mktemp)
tmp2=$(mktemp)

cat ../diminutives/deadjectivals.mbr.dict ../diminutives/denominals.mbr.dict | sort | uniq > $tmp1

python3 coverage.py $tmp1 AN | sort | uniq > diminutives-coverage.tsv

cat ../verbs/clitics/*.dict |sort|uniq > $tmp2

python3 coverage.py $tmp2 V | sort | uniq > clitics-coverage.tsv

rm $tmp1 $tmp2

