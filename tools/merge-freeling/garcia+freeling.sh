sbcl --load garcia+freeling.lisp --eval '(progn (main) (quit))'
awk 'length($3) < 7 && $3 ~ /^A.*/ {print $1,$2,$3 "0"; next} {print}' dicc-AO3_long-1pl.src > dicc-adj.src
cat freeling dicc-adj.src | sort | uniq > garcia+freeling.uniq.src
rm dicc-AO3_long-1pl.src dicc-adj.src

