## delaf
grep "\.A:" Delaf2015v04.dic > adjs.delaf
gf --run < translate-adjs.delaf.gfs
sort -u adjs.bra > adjs.delaf.dict
grep "\.ADV$" Delaf2015v04.dic > adv.delaf
gf --run < translate-adv.delaf.gfs
sort -u adv.bra > adv.delaf.dict
grep "\.N:" Delaf2015v04.dic > nouns.delaf
gf --run < translate-nouns.delaf.gfs
sort -u nouns.bra > nouns.delaf.dict
#grep "\.V:" Delaf2015v04.dic > verbs.delaf
#gf --run < translate-verbs.delaf.gfs
#sort -u verbs.bra verbs.delaf.dict

## garcia
grep " AQ....$" dicc-AO3_long-1pl.src > adjs.bra
awk 'NF{print $0 "0"}' adjs.bra > adjs
gf --run < translate-adjs.gfs
sort -u adjs.bra > adjs.garcia.dict
grep " R.$" dicc-AO3_long-1pl.src > adv
gf --run < translate-adv.gfs
sort -u adv.bra > adv.garcia.dict
grep " N......$" dicc-AO3_long-1pl.src | sort -u > nouns
gf --run < translate-nouns.gfs
sort -u nouns.bra > nouns.garcia.dict
#grep " V......$" dicc-AO3_long-1pl.src | sort -u > verbs
#gf --run < translate-verbs.gfs
#mv verbs.bra verbs.garcia.dict

## freeling
mv adjs.fl adjs
gf --run < translate-adjs.gfs
sort -u adjs.bra > adjs.fl.dict
mv adv.fl adv
gf --run < translate-adv.gfs
sort -u adv.bra > adv.fl.dict
mv nouns.fl nouns
gf --run < translate-nouns.gfs
sort -u nouns.bra > nouns.fl.dict
#mv verbs.fl verbs
#gf --run < translate-verbs.gfs
#sort -u verbs.bra verbs.fl.dict
