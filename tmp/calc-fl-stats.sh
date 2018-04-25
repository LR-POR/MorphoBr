#!/bin/bash

total=$(cat $1 | wc -l)
missing=$(cat $1 | awk -F$'\t' '$3 == "_" {print $3}'| wc -l)

echo "total: $total"
echo "missing: $missing"

echo "scale=4;100*($missing/$total)" | bc

