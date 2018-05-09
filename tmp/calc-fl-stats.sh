#!/bin/bash
tmp=$1

total=$(gzcat $tmp | wc -l)
missing=$(gzcat $tmp | awk '{print $2}' | grep -c MISSING)
indict=$(gzcat $tmp | awk '{print $2}' | grep -c IN-DICT)
rules=$(gzcat $tmp | awk '{print $2}' | grep -c IN-RULES)

echo "total: $total"
echo "missing: $missing"
echo "in dict: $indict"
echo "rules: $rules"

echo -n "missing %: "
echo "scale=4;100*($missing/$total)" | bc
echo -n "in dictionary %: "
echo "scale=4;100*($indict/$total)" | bc
echo -n "rules %: "
echo "scale=4;100*($rules/$total)" | bc
