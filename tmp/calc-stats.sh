#!/bin/bash

total=$(cat $1 | wc -l)
missing=$(cat $1 | grep -c ^missing)
single=$(cat $1 | grep -c ^single)
multiple=$(cat $1 | grep -c ^multiple)

echo "missing"
echo "scale=3;100*($missing/$total)" | bc

echo "single"
echo "scale=3;100*($single/$total)" | bc

echo "multiple"
echo "scale=3;100*($multiple/$total)" |bc
