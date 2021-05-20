# -*- coding: utf-8 -*-

import sys
import re
from nltk import FeatStruct as fs
from os.path import expanduser

morphobr_to_bosque = {
    'A': ['Cat=ADJ'],
    'ADV': ['Cat=ADV'],
    'N': ['Cat=NOUN'],
    'V': ['Cat=VERB'],
    'F': ['Gender=Fem'],
    'M': ['Gender=Masc'],
    'SG': ['Number=Sing'],
    'PL': ['Number=Plur'],
    'NEG': ['Polarity=Neg'],
    'SUPER': ['Degree=Abs'],
    'DIM': ['Degree=Dim'],
    'AUG': ['Degree=Aug'],
    '1': ['Person=1'],
    '2': ['Person=2'],
    '3': ['Person=3'],
    'INF': ['VerbForm=Inf'],
    'GRD': ['VerbForm=Ger'],
    'PTPST': ['VerbForm=Part','Tense=Past'],
    'PRS': ['Mood=Ind','Tense=Pres'],
    'IMPF': ['Mood=Ind','Tense=Imp'],
    'PRF': ['Mood=Ind','Tense=Past'],
    'FUT': ['Mood=Ind','Tense=Fut'],
    'PQP': ['Mood=Ind','Tense=Pqp'],
    'SBJR': ['Mood=Sub','Tense=Pres'],
    'SBJP': ['Mood=Sub','Tense=Imp'],
    'SBJF': ['Mood=Sub','Tense=Fut'],
    'SUBJR': ['Mood=Sub','Tense=Pres'],
    'SUBJP': ['Mood=Sub','Tense=Imp'],
    'SUBJF': ['Mood=Sub','Tense=Fut'],
    'IMP': ['Mood=Imp'],
    'COND': ['Mood=Cod']     
}


def entry_to_fst(entry="simples simples+A+F+PL"):
    ls = re.split(r"[ \+\t]",entry)
    d = [('Form',ls[0]),('Lemma',ls[1])]
    for l in ls[2:]:
        ms = morphobr_to_bosque.get(l.strip())
        for m in ms:
            f = re.split(r"[\=]",m)
            d.append((f[0],f[1]))
    return (ls[0], fs(dict(d)))

def extract_entries(infile):
    with open(infile) as f:
        file =  f.readlines()
        for line in file:
            form, fs = entry_to_fst(line)
            if morpho.get(form):
                morpho[form].append(fs)
            else:
                morpho[form] = [fs]
    f.close()
    file = None
    line = None
    

morpho = {}
for infile in sys.argv[1:]:
    extract_entries(infile)
    print("done")
print(morpho.get("colorido"))
