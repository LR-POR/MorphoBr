#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Leonel Figueiredo de Alencar - Federal University of Ceará
# leonel.de.alencar@ufc.br
# Date: July 2, 2018

"""
This module correct DELAF entries with the V+PRO tag from standard input
by inserting the missing hyphen separating the clitic pronoun from
the verb form in entries like the following:

abluirlhe,abluir.V+PRO:U1s

The output are correct entries, e.g.: 

abluir-lhe,abluir.V+PRO:U1s

Usage: cat INFILE | SeparateHyphen.py > OUTFILE

The module uses the SeparateClitic function from module ConvertDELAF.
Clitic separation is performed using PATTERN1, which presupposes that the
input entries contain the V+PRO tag.
"""

import sys
from ConvertDELAF import *


def main():
    entries=ExtractEntries(sys.stdin)
    for entry in entries:
        sys.stdout.write("%s\n" % SeparateClitic(entry).encode("utf-8"))

if __name__ == '__main__':
	main()
