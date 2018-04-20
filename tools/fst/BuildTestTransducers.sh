#! /bin/bash
# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br
# Date: April 17, 2018

echo "Compiling and testing transducer with Foma"
echo
foma -f build-fst.foma
echo
echo "Applying down Foma's transducer to testfile test-upper.txt"
echo "Output saved in test-upper.foma.out"
echo
foma -r -e "load foma.fst" -e "down < test-upper.txt > test-upper.foma.out" -s
echo
echo "Testing morphological analysis with Foma's transducer,"
echo "applying it up to testfile inho.txt, which contains"
echo "all -inho and -zinho diminutives from DELAF-PB"
echo "Output saved in inho.foma.out"
echo
cat inho.txt | flookup foma.fst > inho.foma.out 
echo
echo "Compiling and testing transducer with XFST"
echo "Applying down XFST's transducer to file test-upper.txt for generation"
echo "and to testfile inho.txt for analysis"
echo "Output of XFST saved in test-upper.xfst.out inho.xfst.out"
xfst -f build-fst.xfst -q
echo
xfst -s xfst.fst -e "down < test-upper.txt > test-upper.xfst.out" -e "up < inho.txt > inho.xfst.out " -stop
