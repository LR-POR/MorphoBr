#! /bin/bash
# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br
# Date: February 17, 2020
# Script for compiling a finite-state transducer (FST) with the Foma package.
# This FST models "-inho" and "-zinho" diminutive fomation in Portuguese.
# It first extracts possible noun and adjective bases from MorphoBr's dict files, converting them to
# spaced-text format:

ExtractWordLemmaPairs.py ~/MorphoBr/nouns/*.dict ~/MorphoBr/adjectives/*.dict

# Then, these bases are converted to FSTs and concatenated with the suffixes and inflectional endings,
# alongside the corresponding morphological tags. The resulting FST undergoes a cascade of alternation rules.# The final FST is written to binary file foma.fst, which can be used for morphological analysis and generation:


foma -f build-fst.foma

# The following command generates all word-parse pairs from this FST:

# BuildPairsFromFomaFST.sh foma.fst
