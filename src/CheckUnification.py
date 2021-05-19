# -*- coding: utf-8 -*-

from nltk import FeatStruct as fs
import re
import json
import conllu
from io import open
from conllu import parse_incr
import sys
import os


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


def check(token_fst,entries):
    """Return the list of conflicting attribute-value pairs between a
    treebank feature structure for a token and a list of dictionary
    entries for this token. If the structures unify with at least one
    entry, return the empty list. Otherwise return the inconsistencies
    collected by means of the function find_error.

    """
    errors=[]
    for entry in entries:
        if entry.unify(token_fst):
            return []
        else:
            errors.append(entry)
    return [find_error(error,token_fst) for error in errors]


def token_to_fst(token,lemma,cat,feats):
    d =[('Form',token),('Lemma',lemma),('Cat',cat)]
    if type(feats) is dict:
        for feat in feats.keys():
            d.append((feat,feats[feat]))
    return fs(dict(d))

def entry_to_fst(entry="simples simples+A+F+PL"):
    ls = re.split(r"[ \+\t]",entry)
    d = [('Form',ls[0]),('Lemma',ls[1])]
    for l in ls[2:]:
        ms = morphobr_to_bosque.get(l.strip())
        for m in ms:
            f = re.split(r"[\=]",m)
            d.append((f[0],f[1]))
    return (ls[0], fs(dict(d)))

def find_error(fs1,fs2):
    attributes=set(fs1.keys()).union(fs2.keys())
    errors=[]
    for k in attributes:
        v1=fs1.get(k)
        v2=fs2.get(k)
        if v1 and v2 and v1 != v2:
            errors.append((k,v1,v2))
    return errors

def print_errors(errors):
    for list_of_errors in errors:
        print(end = "| ")
        for error in list_of_errors:
            print ("atribute '%s': values '%s' and '%s' don't match" % error, end = " ")


# code for reading MorphoBr
morpho = {}

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

def readMorpho(path):
    dirs = ["adjectives","adverbs","nouns","verbs"]
    for d in dirs:
        for root,_, files in os.walk(os.path.join(path,d), topdown=False):
            for file in files:
                extract_entries(os.path.join(root,file))
    return morpho


if __name__ == "__main__":
    morpho = readMorpho("/home/ana/dhbb/MorphoBr")
#    for root,_, files in os.walk("/home/ana/dhbb/dhbb-nlp/udp-mini", topdown=False):
#        for f in files:
#            print("Processing '%s':" % f)
#            with open(os.path.join(root,f), "r", encoding="utf-8") as file:
    with open("/home/ana/dhbb/dhbb-nlp/udp-mini/161.conllu") as file:
        for tks in conllu.parse_incr(file):
            for token in tks:
                if token["upos"] in ["ADJ","ADV","NOUN","VERB"]:
                    tfs = token_to_fst((token["form"]).lower(),token["lemma"],token["upos"],token["feats"])
                    candidates = morpho.get((token["form"]).lower())
                    if candidates:
                        errors = (check(tfs, candidates))
                        if len(errors)>0:
                            print(token, end = " ")
                            print_errors(errors)
                            print("")
                    else:
                        print("token '%s' not found " % token)
    file.close()

"""
TODO:

 - [ ] ler feature structures do morphobr de um json (preparado na lib
       cpdoc/test em Haskell)
 - [ ] comparacao token vs entradas do morphobr com mesma 'form'
 - [ ] saida das diferencas, formatar relatorio

"""            
