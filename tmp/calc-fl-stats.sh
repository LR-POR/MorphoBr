#!/bin/bash

t=$(mktemp)

gzcat $1 | sort | uniq > $t

total=$(cat $t | wc -l)
missing=$(cat $t | awk -F$'\t' '$3 == "_" {print}'| wc -l)
indict=$(cat $t | awk -F$'\t' '$2 == "True" {print}'| wc -l)
rules=$(cat $t | awk -F$'\t' '$2 == "False" && $3 != "_" {print}'| wc -l)

echo "total: $total"
echo "missing: $missing"
echo "in dict: $indict"
echo "rules: $rules"

echo "missing"
echo "scale=4;100*($missing/$total)" | bc
echo "in dictionary"
echo "scale=4;100*($indict/$total)" | bc
echo "rules"
echo "scale=4;100*($rules/$total)" | bc

rm $t
