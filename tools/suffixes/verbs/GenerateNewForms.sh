BASEDIR=$(dirname "$0")
xfst -e "load $BASEDIR/nVerb.fst" -e "print lower-words > LHS.tmp" -e "print upper-words > RHS.tmp" -stop
paste LHS.tmp RHS.tmp > final.tmp
sort final.tmp > verbs.dict
rm LHS.tmp RHS.tmp final.tmp
echo "done."
