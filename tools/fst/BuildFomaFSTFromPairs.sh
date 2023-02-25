#! /bin/bash
# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br

# this script creates stxt files in the directory of the source files,
# not necessarily in the working directory; therefore, it only works if
# the source files are in the working directory
BuildSpacedTextFromFiles.sh "$@"

# WARNING: The script below removes .stxt from working directory
# and .fst files from ./tmp after processing them!

BuildFomaFSTFromSpacedText.sh *.stxt


