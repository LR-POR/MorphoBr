# -*- coding: utf-8 -*-

from __future__ import print_function
from nltk import FeatStruct as fs
import re
import json
import conllu
from io import open
from conllu import parse_incr
import sys
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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



def extract_entries(d, infile):
    with open(infile) as f:
        for line in f.readlines():
            form, fs = entry_to_fst(line)
            if d.get(form):
                d[form].append(fs)
            else:
                d[form] = [fs]


def readMorpho(path):
    adict = {}
    dirs = ["adjectives","adverbs","nouns","verbs"]
    for d in dirs:
        eprint("Loading %s." % d)
        for root,_, files in os.walk(os.path.join(path,d), topdown=False):
            for file in files:
                extract_entries(adict, os.path.join(root,file))
    return adict


def errors2string(errors):
    return " | ".join([ " § ".join([ "%s:%s≠%s" %(e[0],e[1],e[2]) for e in ue]) for ue in errors])

def proc1(morpho, content):
    for sent in conllu.parse_incr(content):
        print("\n%s: %s" % (sent.metadata.get('sent_id'), sent.metadata.get('text')), end = " ")
        for token in sent:
            if token["upos"] in ["ADJ","ADV","NOUN","VERB"]:
                tfs = token_to_fst((token["form"]).lower(),token["lemma"],token["upos"],token["feats"])
                candidates = morpho.get((token["form"]).lower())
                if candidates:
                    errors = check(tfs, candidates)
                    if len(errors)>0:
                        print(" ['%s' %s]" %(token,errors2string(errors)), end = " ")
                else:
                    print(" ['%s' NF]" % token, end = " ")

def proc2(morpho, content):
    for sent in conllu.parse_incr(content):
        sid = sent.metadata.get('sent_id')
        for token in sent:
            if token["upos"] in ["ADJ","ADV","NOUN","VERB"]:
                tid = "%s" % token["id"]
                tfs = token_to_fst((token["form"]).lower(),token["lemma"],token["upos"],token["feats"])
                candidates = morpho.get((token["form"]).lower())
                if candidates:
                    errors = check(tfs, candidates)
                    if len(errors)>0:
                        for ue in errors:
                            for e in ue:
                                print("\t".join([sid,tid,token["form"],e[0],e[1],e[2]]))
                else:
                    print("\t".join([sid,tid,token["form"],'NF','_','_']))


def execute():
    morpho = readMorpho(sys.argv[1])
    for path in sys.argv[2:]:
        with open(path) as content:
            proc2(morpho, content)

def usage():
    print("\n \tpython CheckUnification.py path-morphobr conllu1 conllu2 ... \n\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    else:
        execute()

