#! /bin/bash
# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br 

# This script extract (w,p) pairs from a transducer in Foma's  
# binary format, where w is a word form and p is a parse string,
# separed by a tab. It is also useful for recompiling transducers
# in order to reduce complexity, as described in the following paper:

# Alencar, Leonel F. de et al. JMorpher: A Finite-State Morphological Parser in Java for Android. In: Baptista, Jorge et al. (Eds.). Computational Processing of the Portuguese Language. 11th International Conference, PROPOR 2014. São Carlos/SP, Brazil, October 6-8, 2014. Proceedings. Cham; Heidelberg: Springer, 2014, p. 59-69. 
# (Series: Lecture Notes in Computer Science, Vol. 8775. Subseries: Lecture Notes in Artificial Intelligence) 
# ISBN 978-3-319-09760-2
# http://www.springer.com/computer/ai/book/978-3-319-09760-2?detailsPage=chapter


# Usage: BuildPairsFromFomaFST.sh *.fst
for i in $* 
do 
foma -r -e "load $i" -e "lower-words > $i.lower" -s
sort $i.lower | uniq | flookup $i > $i.pairs

done