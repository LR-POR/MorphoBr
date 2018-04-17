sbcl --load garcia+freeling.lisp --eval '(progn (main) (quit))' 
awk '{print $0,"fl"}' freeling > tmp.fl
awk '{print $0,"mc"}' dicc-AO3_long-1pl.src > tmp.mc
cat tmp.fl tmp.mc | sort | uniq > fl+garcia-uniq.src
rm tmp.fl tmp.mc
