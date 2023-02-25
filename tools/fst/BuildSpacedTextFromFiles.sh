#! /bin/bash
# Author: Leonel Figueiredo de Alencar Araripe
# leonel.de.alencar@ufc.br

# this script creates stxt files in the directory of the source files,
# not in the working directory

for i in $* 
do 
BuildSpacedText.py $i
done