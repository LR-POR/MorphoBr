#!/bin/bash
# don't forget to change CRLF to LF!
# tr -d '\r' < Delaf2015v04.dic > delaf.dic

# adjectives
grep -F ".A:" $1 > delaf.adj

# adverbs
grep -F ".ADV$" $1 > delaf.adv

# nouns
grep -F ".N:" $1 | # select nouns
#remove uppercase lemmas (Gloria)
    grep -v ",[A-Z]" > delaf.nouns

# simple verbs
grep -F ".V:" $1 | # select simple verbs
    sed "s/:,/,/" | # rm entries like mantinhas:,manter.V:I2s
# sorri,sorrir.V:Y2S -> sorri,sorrir.V:Y2s
    sed "s/2S$/2s/" > delaf.verbs

# verbs with clitics
grep -F ".V+PRO:" $1 | # select verbs with clitics
# rm spurious colon like in abstinhas:-lhe,abster.V+PRO:I2s
    sed "s/:-/-/" > delaf.clitics
