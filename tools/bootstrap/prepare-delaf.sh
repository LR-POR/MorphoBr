#!/bin/bash
# first argument is path to delaf dictionary

# don't forget to change CRLF to LF!
# tr -d '\r' < Delaf2015v04.dic > delaf.dic

function splitW31 {
    # split entries what end in W31 but should be two entries, one
    # with W3s and the other with W1s
    sed "s/\\(.*W\\)31$/\\13s\\n\\11s/"
}

# adjectives
grep -F ".A:" "$1" > delaf.adj

# adverbs
grep -F ".ADV$" "$1" > delaf.adv

# nouns
grep -F ".N:" "$1" | # select nouns
#remove uppercase lemmas (as in Gloria)
    grep -v ",[A-Z]" > delaf.nouns

# # simple verbs
 grep -F ".V:" "$1" | # select simple verbs
     sed "s/:,/,/" | # rm entries like mantinhas:,manter.V:I2s
# # sorri,sorrir.V:Y2S -> sorri,sorrir.V:Y2s
     sed "s/2S$/2s/" | # split entries like abstrair,abstrair.V:W31
     splitW31 > delaf.verbs

# verbs with clitics
grep -F ".V+PRO:" "$1" | # select verbs with clitics
    sed "s/:-/-/" | # rm spurious colon like in abstinhas:-lhe,abster.V+PRO:I2s
    splitW31 |
    # add hyphen where it should exist amarnos -> amar-nos
    SeparateHyphen.py > delaf.clitics
