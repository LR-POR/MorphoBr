#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Leonel Figueiredo de Alencar - Federal University of Ceará
# leonel.de.alencar@ufc.br
# Date: June 27, 2018
"""
This module annotates enclitic or mesoclitic pronouns in entries in the MBR format

Usage: cat infile.mbr | AnnotateClitics.py > outfile.mbr

It reads entries in the MBR format from standard input and substitutes
the +PRO tag for tags representing the lemma and morpho-syntactic features
of the pronouns. The result is written to standard output.
For example, an entry like

degustares-lhe	degustar+V+PRO+INF+2+SG

is converted to

degustares-lhe	degustar+V.ele.DAT.3.SG+SBJF+2+SG

Tag conversion is performed by the AnnotateClitic function from
the module ConvertDELAF.py. Ambiguity of clitic "nos" is also handled. 
For more details, see the respective module documentation.
"""
import sys
from ConvertDELAF import *


def main():
    entries=ExtractEntries(sys.stdin)
    for entry in entries:
        if HasClitic(entry):
            parts=ParseEntry(entry,r"\t|\+")
            word,lemma,cat,feats=parts[0],parts[1],parts[2],parts[4:]
            print AnnotateClitic(word,lemma,cat,feats).encode("utf-8")
        else:
            print entry.encode("utf-8")
if __name__ == '__main__':
	main()
