#!/bin/bash

HASH=c812f903a9b61ddaafda9bfcf2595a990a394a42722428e7d371d8c55bb93bfb
EXE=code/.stack-work/install/x86_64-osx/$HASH/9.2.6/bin/code-exe
TMP=tmp

for f in nouns/*.dict; do $EXE -m $f >> $TMP/nouns.stxt ; done
for f in verbs/*.dict; do $EXE -m $f >> $TMP/verbs.stxt ; done
for f in clitics/*.dict; do $EXE -m $f >> $TMP/clitics.stxt ; done
for f in adjectives/*.dict; do $EXE -m $f >> $TMP/adjectives.stxt ; done
for f in adverbs/*.dict; do $EXE -m $f >> $TMP/adverbs.stxt ; done

foma -f compile.foma

rm $TMP/*.stxt
