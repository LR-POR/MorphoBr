#! /bin/bash
# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br

echo "clear" > script$$.foma
# Usage: BuildFomaFSTFromSpacedText.sh *.stxt

# WARNING: This script removes generated .stxt files from working directory
# and .fst files from temporary directory after processing them!

TEMP=tmp$$
mkdir ${TEMP}
for i in $*
  do
    foma -r -e "read spaced-text $i" -e "save stack ${TEMP}/$i.fst" -s
    echo "load ${TEMP}/$i.fst" >> script$$.foma
    # remove stxt files
  #  rm $i
  done
echo "Value of i $i"
echo "union" >> script$$.foma
echo "save stack foma$$.fst" >> script$$.foma
echo "write att > foma$$.att" >> script$$.foma
echo "read att foma$$.att" >> script$$.foma
foma -f script$$.foma
# rm ${TEMP}/*.fst
# rm script$$.foma
# rm -d ${TEMP}
