#!/usr/bin/env python3
"""Converte arquivos .dict (forma<TAB>lema+TAG+TAG...) no formato spaced-text
do foma: a forma e o lema letra a letra, cada etiqueta (+TAG) como um símbolo.
Substitui o conversor em Haskell que ficava em code/ (ver #168).

Uso: tools/dict2stxt.py ARQUIVO... > saída.stxt
"""
import sys

for fn in sys.argv[1:]:
    with open(fn, encoding="utf-8", newline="") as f:
        for line in f:
            line = line.rstrip("\r\n")
            if not line:
                continue
            form, analysis = line.split("\t")
            lemma, *tags = analysis.split("+")
            sys.stdout.write(" ".join(form) + "\n"
                             + " ".join(list(lemma) + ["+" + t for t in tags]) + "\n\n")
