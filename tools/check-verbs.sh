
echo DELAS
grep --color=never -o -E "\t[^+]+\+V" *pairs | sort | uniq -c > forms.count
grep -v "71" forms.count | wc -l
awk 'BEGIN {MAIS=0;MENOS=0;ESPERADO=0} $1 > 71 {MAIS+=1} $1 < 71 {MENOS+=1} $1 == 71 {ESPERADO+=1} END { print MAIS,MENOS,ESPERADO}' forms.count 
rm forms.count
echo

echo DELAS + GFL
grep --color=never -o -E "\t[^+]+\+V" *.{pairs,gfl} | sort | uniq -c > forms.count
grep -v "71" forms.count | wc -l
awk 'BEGIN {MAIS=0;MENOS=0;ESPERADO=0} $1 > 71 {MAIS+=1} $1 < 71 {MENOS+=1} $1 == 71 {ESPERADO+=1} END { print MAIS,MENOS,ESPERADO}' forms.count
rm forms.count
echo

echo DELAS + GFL - filter
grep --color=never -Ev ".*mo[[:space:]].*\+V\+[A-Z]+\+1\+PL" verbs.diff.gfl > verbs.diff.gfl.filtrados
grep --color=never -o -E "\t[^+]+\+V" *.{pairs,filtrados} | sort | uniq -c > forms.count
awk 'BEGIN {MAIS=0;MENOS=0;ESPERADO=0} $1 > 71 {MAIS+=1} $1 < 71 {MENOS+=1} $1 == 71 {ESPERADO+=1} END { print MAIS,MENOS,ESPERADO}' forms.count
rm forms.count verbs.diff.gfl.filtrados
