#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 12:43:21 2021

@author: leonel
"""
import re
from os.path import expanduser
sep=re.compile(r"\t|\+")

def extract_entries(infile):
    with open(infile) as f:
        return [line.strip() for line in f.readlines()]
        
def parse_entry(entry):
    return sep.split(entry)

def build_entry_dict(form,lemma,pos,feats):
    entry_dict={}
    entry_dict["form"]=form
    entry_dict["lemma"]=lemma
    entry_dict["pos"]=pos
    entry_dict["feats"]=feats
    return entry_dict
    
def build_entry_dict_list(entries):
    entry_dict_list=[]
    for entry in entries:
        entry_dict={}
        parts=parse_entry(entry)
        entry_dict["form"]=parts[0]
        entry_dict["lemma"]=parts[1]
        entry_dict["pos"]=parts[2]
        entry_dict["feats"]=parts[3:]
        entry_dict_list.append(entry_dict)
    return entry_dict_list

def build_lemma_dict(entry_dict_list):
    """build dictionary mapping (lemma,pos) to (form,feats)"""
    lemma_dict={}
    for entry in entry_dict_list:
        key=(entry["lemma"],entry["pos"])
        value=(entry["form"],entry["feats"])
        if lemma_dict.get(key):
            lemma_dict[key].append(value)
        else:
            lemma_dict[key]=[value]
    return lemma_dict

def build_forms_dict(form_feats_list):
    """
    forms=build_forms_dict(lemma_dict['simples','A'])
    forms['simples']
    [['F', 'PL'], ['F', 'SG'], ['M', 'PL'], ['M', 'SG']]
    """
    forms={}
    for form,feats in form_feats_list:
        if not forms.get(form):
           forms[form]=[feats] 
        else:
            forms[form].append(feats)
    return forms
    

def common_feats(feats_lists):
    """
    return a list with the common features of a list of 
    feature lists, e.g.
    
    common_feats([['F', 'PL'], ['F', 'SG'], ['M', 'PL'], ['M', 'SG']])
    
    []
    """
    set_list=[set(feats) for feats in feats_lists]
    for s in set_list[1:]:
        set_list[0].intersection_update(s)
    return list(set_list[0])

def simplify(lemma_dict):  
    for lemma,pos in lemma_dict.keys():
        forms=build_forms_dict(lemma_dict[lemma,pos]) 
        for form in forms.keys():
            feats_lists=forms[form]
            entry="%s\t%s+%s+" % (form,lemma,pos)
            if len(feats_lists) > 1:
                feats=common_feats(feats_lists)
            else:
                feats=feats_lists[0]
            print("%s%s" % (entry,"+".join(feats)))
            
def main(infile=expanduser("~/scripts/check-tools/mini.txt")):
    entries=extract_entries(infile)
    entry_dict_list=build_entry_dict_list(entries)
    lemma_dict=build_lemma_dict(entry_dict_list)
    simplify(lemma_dict)
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        main()
    else:
        for infile in sys.argv[1:]:
            main(infile)

