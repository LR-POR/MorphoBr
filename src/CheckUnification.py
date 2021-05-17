# -*- coding: utf-8 -*-

from nltk import FeatStruct as fs
import re
import json
import conllu
from io import open
from conllu import parse_incr
import sys

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
    ls = re.split(r"[ \+]",entry)
    d = [('Form',ls[0]),('Lemma',ls[1])]
    for l in ls[2:]:
        ms = morphobr_to_bosque.get(l)
        for m in ms:
            f = re.split(r"[\=]",m)
            d.append((f[0],f[1]))
    return fs(dict(d))


def find_error(fs1,fs2):
    attributes=set(fs1.iterkeys()).union(fs2.iterkeys())
    errors=[]
    for k in attributes:
        v1=fs1.get(k)
        v2=fs2.get(k)
        if v1 and v2 and not v1 == v2:
            errors.append((k,v1,v2))
        return errors

def pprint_errors(errors):
    for list_of_errors in errors:
        for error in list_of_errors:
            print ("attribute '%s': values '%s' and '%s' don't match" % error)


def find_candidates(tfs, dicionario):
    """dado um token, recupera do dict (form -> [fs]). 
      
       [fs for fs in dict[tfs.get("form")] if fs.get("pos") == tfs.get("pos")] """
    return dicionario[tfs.get("form")]

# code for demo            
            
def check_unification(fs1,fs2):
    msg="feature structures%s unify"
    if fs1.unify(fs2):
         print (msg % "")
    else:
        print (msg % " don't")
        find_error(fs1,fs2)

def demo():
    print ("%s\n\n%s\n" % (TOKEN,ENTRY))
    check_unification(TOKEN, ENTRY)
    print ("\n%s\n\n%s\n" % (ERROR,ENTRY))
    check_unification(ERROR, ENTRY)
    print ("\n%s\n" % ("in case of unification nothing is printed"))
    check(TOKEN, ENTRIES)
    print ("\n%s\n" % ("showing why unification failed"))
    ENTRIES.pop(0)
    check(TOKEN, ENTRIES)


def readMorpho(dir):
    """  ler arquivos dict dentro de adjectives, nouns, verbs, adverbs. """
    dicionario = {}
    return dicionario


with open(sys.argv[1], "r", encoding="utf-8") as file:
    dicionario = readMorpho("/Users/ar/work/morpho-br")
    for tks in conllu.parse_incr(file):
        for token in tks:
            print("")
            tfs = token_to_fst(token)
            candidates = find_candidates(tfs, dicionario)
            res = check(tfs, candidates)
            print(res)


"""
TODO:

 - [ ] ler feature structures do morphobr de um json (preparado na lib
       cpdoc/test em Haskell)
 - [ ] comparacao token vs entradas do morphobr com mesma 'form'
 - [ ] saida das diferencas, formatar relatorio

"""            
