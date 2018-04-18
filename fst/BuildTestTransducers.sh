#! /bin/bash
# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br

echo "Compiling transducer with Foma"
echo
foma -f build-suff.foma
echo
echo "Applying down transducer to testfile test-upper.txt"
foma -r -e "load suff02-foma.fst" -e "down < test-upper.txt" -s
echo
echo "Compiling and testing transducer with XFST"
echo "Output of applying up in inho.out"
xfst -f build-suff.xfst -q