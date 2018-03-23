#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br

# Usage: python BuildPairsFromDELAF.py infile1 [infile2 ... infilen]

""""Module for building word-parse pairs from DELAF-PB, converting entries in the format

agendas,agenda.N:fp

to an intermediate format used to compile lexical transducers with XFST or FOMA, using the respective
spaced-text compilers:

agendas	agenda+N+F+PL

The module also substitutes the PRO tag in verb forms with an enclitic or mesoclitic pronoun for tags 
representing the lemma and morpho-syntactic features of these pronouns. Thus, convertions like the following
are performed:

degustares-lhe,degustar.V+PRO:W2s
degustares-lhe	degustar+V.ele.DAT.3.SG+SBJF+2+SG

Entries in this intermediate format, in turn, can be converted to spaced-text using the BuildSpacedText.py module.
The tag convertions are based on the mappings defined in the dictionaries stored in the global variables TAG_MAPPING and CLITIC_MAPPING.
The regular expression pattern in the global variable SEPARATOR is used for splitting 
entries in its component parts, i.e. word form, lemma, lexical category and morpho-syntactic features:

mantinham manter V I3p

This separator also handles incorrectly encoded entries
from DELAF-PB like the following, where the first colon is spurious:

mantinhas:,manter.V:I2s

A spurious hyphen in cases like abstinhas:-lhe,abster.V+PRO:I2s is eliminated by the function ConvertEntry()
"""

import re,sys,os
from cPickle import load,dump
from BuildSpacedText import extract_entries

SEPARATOR=r"[,.:]+"
PATH_TO_MAPPING_FILE=os.path.expanduser("~/morphtools/tag_mapping.txt")
PATH_TO_MAPPING_FILE2=os.path.expanduser("~/morphtools/clitics.txt")

PRO="+PRO"

def UnpickleMapping(infile):
    f=open(infile,"rb")
    dic=load(f)
    f.close()
    return dic

TAG_MAPPING=UnpickleMapping(os.path.expanduser("~/morphtools/tag_mapping.pkl"))
CLITIC_MAPPING=UnpickleMapping(os.path.expanduser("~/morphtools/clitics.pkl"))

def ExtractMapping(mapping_file=PATH_TO_MAPPING_FILE):
    return extract_entries(mapping_file)

def ConvertTagsetFromFile(mapping_file=PATH_TO_MAPPING_FILE):
    tag_mapping=dict()
    lines=ExtractMapping(mapping_file)
    for line in lines:
        tags=re.split(r"\s+",line)[:2]
	tag_mapping[tags[0]]=tags[1]
    return tag_mapping

#def CliticMapping(infile):
#    return ConvertTagsetFromFile(infile)

#CLITIC_MAPPING=CliticMapping(PATH_TO_MAPPING_FILE2)

def PickleMapping(mapping,outfile):
    f=open(outfile,"wb")
    dump(mapping,f,-1)
    f.close()

def BuildMappings(*infiles):
    for f in infiles:
        PickleMapping(ConvertTagsetFromFile(f),"%s.pkl" % f.split(".")[0])

def HasClitic(cat):
    return PRO in cat

def ExtractClitic(word):
    for k in CLITIC_MAPPING.keys():
        # a clitic immediately follows a hyphen in word end position in enclisis or
        # appears between hyphens in the case of mesoclisis
	if re.search(r"-%s(-|\b)" % k, word):
		return k

def EndsInNasalDiphthong(word):
    pattern=r"\w+([õã][eo]\b|m\b)".decode("utf-8")
    if re.match(pattern,word):
        return True
    else:
        return False

def AppendCliticFeatures(word,cat):
    return "%s.%s" % (cat.split(PRO)[0], CLITIC_MAPPING.get(ExtractClitic(word)))

def ConcatenateFeatures(dic,feats):
    return "+".join([dic[f] for f in list(feats)])

def ConvertEntry(entry,dic):
    # eliminating spurious hyphen in cases like abstinhas:-lhe,abster.V+PRO:I2s
    error=":-"
    corr="-"
    if error in entry:
        entry=entry.replace(error,corr)
    parts=re.split(SEPARATOR,entry)
    # if cat is an uninflected category like ADV
    if len(parts) == 3:
        word,lemma,cat=parts
        return "%s\t%s+%s" % (word,lemma,cat)
    # if entry is split in less than 3 or more than 4 parts,
    # then there must be something wrong in entry (e.g. due to bad formating)
    if len(parts) != 4:
        print entry
        return None
    word,lemma,cat,feats=parts 
    # if +PRO in cat, then delete +PRO and append clitic features to cat
    if HasClitic(cat):
        cat_list= AppendCliticFeatures(word,cat).split("/")
        # print cat_list
        # handling ambiguity of clitic "nos" after nasal diphthong
        if len(cat_list)==2:
            if EndsInNasalDiphthong(word):
                cat_list[1]="%s.%s" % (cat_list[0].split(".")[0],cat_list[1])
                entries=[]
                for c in cat_list:
                    entries.append("%s\t%s+%s+%s" % (word,lemma,c,ConcatenateFeatures(dic,feats)))
                return "\n".join(entries)
            else:
                cat=cat_list[1]
        else:
            cat=cat_list[0]
    return "%s\t%s+%s+%s" % (word,lemma,cat,ConcatenateFeatures(dic,feats))

def ConvertEntriesFromFile(infile,tag_mapping=TAG_MAPPING):
    entries=extract_entries(infile)
    return [ConvertEntry(e,tag_mapping) for e in entries]
    

def WriteFile(entries,infile):
    f=open("%s.pairs" % infile, "w")
    for e in entries:
        f.write("%s\n" % e.encode("utf-8"))
    f.close()

def main(): 
    for file in sys.argv[1:]:
        WriteFile(ConvertEntriesFromFile(file),file)

if __name__ == '__main__':
	main()
