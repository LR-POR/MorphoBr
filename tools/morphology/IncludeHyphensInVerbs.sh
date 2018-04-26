#! /bin/bash
# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br
# Date: April 26, 2018

# uniq.txt contains all verbs with clitics from DELAF_PB
grep -Ev "\-" uniq.txt > no_hyphens.txt

# extracting all types of clitics from the converted files
grep -E "\-" uniq.*.pairs | awk -F- '{print $2}' | awk '{print $1}' | sort | uniq > clitics.txt

# testing regex matching all clitics from clitics.txt
grep -E "[ln]?[ao]s?|lhes?|[mst]e|vos" clitics.txt  > clitics02.txt
diff -bq clitics.txt clitics02.txt

# inserting a hyphen separating verb and clitic

sed -E "s@(^.+)([ln]?[ao]s?|lhes?|[mst]e|vos)(,)@\1\-\2\3@g" no_hyphens.txt > with_hyphens.txt
