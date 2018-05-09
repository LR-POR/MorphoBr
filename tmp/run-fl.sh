set -x

tmp1=$(mktemp)
python3 coverage.py ../diminutives/deadjectivals.mbr.dict A > $tmp1
python3 coverage.py ../diminutives/denominals.mbr.dict N >> $tmp1

cat $tmp1 | sort | uniq > diminutives-coverage.tsv

tmp2=$(mktemp)

cat ../verbs/clitics/*.dict |sort|uniq > $tmp2

python3 coverage.py $tmp2 V | sort | uniq > clitics-coverage.tsv

rm $tmp1 $tmp2

