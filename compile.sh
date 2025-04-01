#!/bin/bash

HASH=8c6f9cc9675f5af6be43a7692a4d501a5dae79e7c0cc307fa2b861b2cfff82e4
EXE=code/.stack-work/install/aarch64-osx/$HASH/9.2.6/bin/code-exe
TMP=tmp

for f in nouns/*.dict; do $EXE -m $f >> $TMP/nouns.stxt ; done
for f in verbs/*.dict; do $EXE -m $f >> $TMP/verbs.stxt ; done
for f in clitics/*.dict; do $EXE -m $f >> $TMP/clitics.stxt ; done
for f in adjectives/*.dict; do $EXE -m $f >> $TMP/adjectives.stxt ; done
for f in adverbs/*.dict; do $EXE -m $f >> $TMP/adverbs.stxt ; done

foma -f compile.foma

rm $TMP/*.stxt
