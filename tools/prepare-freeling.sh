#!/bin/bash
# first argument if path to directory where freeling dictionary files
# are, with their original names

# adjectives
# change C as diminutive tag to D (as is in nouns)
sed "s/ AQC/ AQD/" adjs > fl.adjectives

# adverbs
mv adv fl.adverbs

# nouns
# correct nouns with wrong C tag such as habeas-corpus
sed "s/ NCMC/ NCMN/" nouns > fl.nouns

# verbs
mv verbs fl.verb
