#!/bin/bash

awk '
BEGIN {  print "import MorphoMbr.gf" }
{
    gsub(/\+/, " +", $2) ; # add space before plus sign
    gsub(/\./, " . ", $2) ; # add space between clitics elements
    print "p \"" $1 " &t " $2 "\"" ; # add &t in lieu of TAB
}' "$1" | gf --crun | grep -n "The parser"
