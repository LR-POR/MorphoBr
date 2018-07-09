#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# new version of Bruno Cuconato's script
# changes made by Leonel F. de Alencar
import codecs
import re
from ConvertDELAF import EndsInNasalDiphthong

def parse_entry(e):
    [f,ts] = e.split("\t")
    parts = ts.split("+")
    return (f,parts[0],parts[1:])

def enrich_clitic(ve):
    def clitic_tags(f):
        cmap = {"a":[".ele.ACC.3.F.SG"],"as":[".ele.ACC.3.F.PL"],"la":
                [".ele.ACC.3.F.SG"],"las":[".ele.ACC.3.F.PL"],"lhe":
                [".ele.DAT.3.SG"],"lhes":[".ele.DAT.3.PL"],"lo":
                [".ele.ACC.3.M.SG"],"los":[".ele.ACC.3.M.PL"],"me":
                [".eu.AD.1.SG"],"na":["ele.ACC.3.F.SG"],"nas":
                [".ele.ACC.3.F.PL"],"no":[".ele.ACC.3.M.SG"],"nos":
                [".nós.AD.1.PL".decode("utf-8"), ".ele.ACC.3.M.PL"], # the "nós" reading is more basic, so it is now the first element in the list
                "o":["ele.ACC.3.M.SG"],"os":[".ele.ACC.3.M.PL"],"se":
                [".ele.REFL"],"te":["tu.AD.2.SG"],"vos":[".vós.AD.2.PL".decode("utf-8")]}
        # the original version doesn't cope with mesoclisis, e.g. "ababadar-nos-emos	ababadar+V+PRO+FUT+1+PL"
        # i = f.rfind("-")
        parts=re.split(r"\-",f)
        if len(parts) == 1:
            return [""]
        else:
            verb_form=parts[0]
            c = parts[1]
            clitic_feats=cmap[c]
            if len(clitic_feats) == 2 and EndsInNasalDiphthong(verb_form): # handling ambiguity of "nos"
                return clitic_feats
            else:
                return [clitic_feats[0]]

    f, l, fs = ve
    #cl, *fs = fs
    cl= fs.pop(0)
    if cl == "V": # this condition is two weak because there are potentially verb forms with hyphen which doens't contain any clitic (e.g. "pré-selecionar"; one should instead check for the existence of a PRO tag in the input entry
        return [(f, l, [(cl + cts)] + fs) for cts in clitic_tags(f)]
    else:
        return [ve]

def print_entry(pe):
    f, l, fs = pe
    return "%s\t%s" % (f,"+".join([l]+fs))

def read_dict(fp):
    with codecs.open(fp, mode='r', encoding="utf8") as fh:
        for l in fh:
            yield l

if __name__ == "__main__":
    from sys import argv
    ls = read_dict(argv[1])
    for l in ls:
        e = parse_entry(l)
        ee = enrich_clitic(e)
        for i in ee:
		print print_entry(i)
