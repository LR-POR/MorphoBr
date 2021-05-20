# -*- coding: utf-8 -*-

from nltk import FeatStruct as fs
import re
import json
import conllu
from io import open
from conllu import parse_incr
import sys
import os

with open('morphobr_to_bosque.json') as f:
    morphobr_to_bosque = json.load(f)


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
            errors.append([k,v1,v2])
    return errors

def print_errors(errors):
    for list_of_errors in errors:
        for error in list_of_errors:
            print(error[0],end = ":")
            print(error[1],end = "!=")
            print(error[2],end = " ")
        print("§",end = " ")


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


# sys.argv[1]: diretório MorphoBr
# sys.argv[2:]: arquivos conllu

if __name__ == "__main__":
    morpho = readMorpho(sys.argv[1])
#    for root,_, files in os.walk("/home/ana/dhbb/dhbb-nlp/udp-mini", topdown=False):
#        for f in files:
#            print("Processing '%s':" % f)
#            with open(os.path.join(root,f), "r", encoding="utf-8") as file:
    for path in sys.argv[2:]:
        with open(path) as file:
            print("Processing '%s':" % path)
            for tks in conllu.parse_incr(file):
                print(tks.metadata.get('text'), end = " ")
                for token in tks:
                    if token["upos"] in ["ADJ","ADV","NOUN","VERB"]:
                        tfs = token_to_fst((token["form"]).lower(),token["lemma"],token["upos"],token["feats"])
                        candidates = morpho.get((token["form"]).lower())
                        if candidates:
                            errors = (check(tfs, candidates))
                            if len(errors)>0:
                                print("| '%s' " %token, end = " " )
                                print_errors(errors)
                        else:
                            print("| token '%s' not found" % token, end = " ") 
                print("")
        file.close()

"""
TODO:

 - [ ] ler feature structures do morphobr de um json (preparado na lib
       cpdoc/test em Haskell)
 - [ ] comparacao token vs entradas do morphobr com mesma 'form'
 - [ ] saida das diferencas, formatar relatorio

"""            
