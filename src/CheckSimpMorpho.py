# -*- coding: utf-8 -*-

from __future__ import print_function
from nltk import FeatStruct as fs
import re
import json
from io import open
import sys
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

with open('morphobr_to_bosque.json') as f:
    morphobr_to_bosque = json.load(f)

def check(token_fst,entries):
    errors=[]
    for entry in entries:
        if entry.unify(token_fst):
            return []
        else:
            errors.append(entry)
    return [find_error(error,token_fst) for error in errors]

def find_error(fs1,fs2):
    attributes=set(fs1.keys()).union(fs2.keys())
    errors=[]
    for k in attributes:
        v1=fs1.get(k)
        v2=fs2.get(k)
        if v1 and v2 and v1 != v2:
            errors.append([k,v1,v2])
    return errors

def entry_to_fst(entry="simples simples+A+F+PL"):
    ls = re.split(r"[ \+\t]",entry)
    d = [('Form',ls[0]),('Lemma',ls[1])]
    for l in ls[2:]:
        ms = morphobr_to_bosque.get(l.strip())
        for m in ms:
            f = re.split(r"[\=]",m)
            d.append((f[0],f[1]))
    return (ls[0], fs(dict(d)))

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
    dirs = ["adjectives","nouns"]
    for d in dirs:
        eprint("Loading %s." % d)
        for root,_, files in os.walk(os.path.join(path,d), topdown=False):
            for file in files:
                extract_entries(adict, os.path.join(root,file))
    return adict

def errors2string(errors):
    return " | ".join([ " § ".join([ "%s:%s≠%s" %(e[0],e[1],e[2]) for e in ue]) for ue in errors])

def proc(simp,path):
    dirs = ["adjectives","nouns"]
    for d in dirs:
        for root,_, files in os.walk(os.path.join(path,d), topdown=False):
            for file in files:
                eprint("Testing %s." % d)
                with open(os.path.join(root,file)) as f:
                    for line in f.readlines():
                        form, fs = entry_to_fst(line)
                        candidates = simp.get(form)
                        if candidates:
                            errors = check(fs, candidates)
                            if len(errors)>0:
                                print(" ['%s' %s]" %(form,errors2string(errors)), end = " ")
                        else:
                            print(" ['%s' NF]" % form, end = " ")

morpho = readMorpho(sys.argv[1])
proc(morpho,sys.argv[2])



