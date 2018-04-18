#!/bin/bash

# meant to be run from ROOT directory of the morphoBR repository

function cat-dict {
    OUTPUT=$(echo $1 | sed 's/\//-/g')
    cat $1/*.dict > $OUTPUT.dict
}

# adjectives
cat-dict adjectives
# adverbs
cat-dict adverbs
# nouns
cat-dict nouns
# noun diminutives
cat-dict diminutives/nouns
# verbs
cat-dict verbs
# verb clitics
cat-dict verbs/clitics
