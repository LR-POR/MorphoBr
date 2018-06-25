#!/bin/bash

# $1 : directory where delaf and freeling dictionaries are.
## assumes upstream sources are unmodified, including filenames.

###
## corrections

# CRLF -> LF
tr -d '\r' < Delaf2015v04.dic > delaf.dic

# correct delaf errors
bash prepare-delaf.sh "$1"

# correct freeling errors
bash prepare-freeling.sh "$1"

###
## conversion

