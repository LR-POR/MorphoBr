#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Author: Leonel Figueiredo de Alencar - Federal University of Ceará
# leonel.de.alencar@ufc.br
# Date: June 27, 2018

# Usage: ConvertDELAF.py infile1 [infile_2 ... infile_n]

""""Module for building word-parse pairs from DELAF-PB, converting entries in the format

agendas,agenda.N:fp

to MorphoBr format:

agendas	agenda+N+F+PL

Ouput files have the extension .mbr. 
Entries in the MBR format can be converted to spaced-text with the BuildSpacedText.py module. Spaced-text, in turn, compiles into lexical transducers with XFST or FOMA, using the respective spaced-text compilers.
Tag conversions are based on the mappings defined in the dictionaries stored in the global variables TAG_MAPPING and CLITIC_MAPPING. Put these files in the directory specified in DATA_DIR or edit this variable to point to where these files are in your system. 

The regular expression pattern in the global variable SEPARATOR is used for splitting 
entries in its component parts, i.e. word form, lemma, lexical category and morpho-syntactic features, e.g.:

mantinham manter V I3p

This separator also handles incorrectly encoded entries
from DELAF-PB like the following, where the first colon is spurious:

mantinhas:,manter.V:I2s

A spurious colon in cases like abstinhas:-lhe,abster.V+PRO:I2s is eliminated by the function CorrectEntry()
"""

import re,sys
from os.path import join,expanduser
from cPickle import load,dump

DATA_DIR=expanduser("~/morphtools_data")
TAGS="tag_mapping"
CLITICS="clitics"
PATH_TO_MAPPING_FILE=join(DATA_DIR,"%s.%s" % (TAGS,"txt"))
PATH_TO_MAPPING_FILE2=join(DATA_DIR,"%s.%s" % (CLITICS,"txt"))
EXTENSION="mbr" # output file extension
SEPARATOR=r"[,.:]+"
PRO="PRO"
# PATTERN=r"(^[^-]+)(vos|n[oa]s?|l[oa]s?|lhes?|me|se|te)(,.+\V\+PRO)"
PATTERN1=r"(^[^-]+)(vos|n[oa]s?|l[oa]s?|lhes?|me|se|te)(,)"
PATTERN2=r"(^[^-]+)([oa]s?)(,)"

def UnpickleMapping(infile):
    f=open(infile,"rb")
    dic=load(f)
    f.close()
    return dic

TAG_MAPPING=UnpickleMapping(join(DATA_DIR,"%s.%s" % (TAGS,"pkl")))
CLITIC_MAPPING=UnpickleMapping(join(DATA_DIR,"%s.%s" % (CLITICS,"pkl")))

def OpenFile(filename):
    return open(filename,"rU")

def IgnoreLine(line):
	return len(line.strip()) > 0 and not line.strip().startswith("#")

def ExtractEntries(file):
	return [line.strip().decode("utf-8") for line in file if IgnoreLine(line)]

def ExtractMapping(filename=PATH_TO_MAPPING_FILE):
    return ExtractEntries(OpenFile(filename))

def ConvertTagsetFromFile(filename=PATH_TO_MAPPING_FILE):
    tag_mapping=dict()
    lines=ExtractMapping(filename)
    for line in lines:
        tags=re.split(r"\s+",line)[:2]
	tag_mapping[tags[0]]=tags[1]
    return tag_mapping

def PickleMapping(mapping,outfile):
    f=open(outfile,"wb")
    dump(mapping,f,-1)
    f.close()

def BuildMappings(*infiles):
    for f in infiles:
        PickleMapping(ConvertTagsetFromFile(f),"%s.pkl" % f.split(".")[0])

def HasClitic(entry):
    return "+%s+" % PRO in entry

def ExtractClitic(word):
    for k in CLITIC_MAPPING.keys():
        # a clitic immediately follows a hyphen in word end position in enclisis or
        # appears between hyphens in the case of mesoclisis
	if re.search(r"-%s(-|\b)" % k, word):
		return k

def EndsInNasalDiphthong(word):
    pattern=r".+([õã][eo]\b|m\b)".decode("utf-8")
    if re.match(pattern,word):
        return True
    else:
        return False

def AppendCliticFeatures(word,cat):
    return "%s.%s" % (cat, CLITIC_MAPPING.get(ExtractClitic(word)))

def ConcatenateFeatures(feats):
    return "+".join(feats)

def ConvertFeatures(feats,dic=TAG_MAPPING):
    return [dic.get(f,f) for f in feats]

def SeparateClitic(entry):
    """Separate clitic from verb form in entries like abluirlhe,abluir.V+PRO:U1s,
    returning entries like abluir-lhe,abluir.V+PRO:U1s. Clitic separation is performed in two steps: first, clitics beginning with a consonant are separated; then, clitics beginning with a vowel are separated. This is necessary to prevent unwanted separations like
zuirn-os,zuir.V+PRO:W3s instead of zuir-nos,zuir.V+PRO:W3s, since the form of latter
type clitics are contained in the ones of the former."""
    return re.sub(PATTERN2,r"\1-\2\3",re.sub(PATTERN1,r"\1-\2\3",entry))

def CorrectEntry(entry):
    "Eliminate spurious colon in cases like abstinhas:-lhe,abster.V+PRO:I2s"
    error=":-"
    corr="-"
    if error in entry:
        entry=entry.replace(error,corr)
    return entry

def EditEntry(entry):
    "Substitute ambiguous letter S, which represents both the superlative of adjectives and the present subjunctive of verbs, for E in the former case."
    return re.sub(r":S([mf][sp]$)",r":E\1",entry)

def ParseEntry(entry,sep=SEPARATOR):
    return re.split(sep,EditEntry(CorrectEntry(entry)))

def AnnotateClitic(word,lemma,cat,feats):
    """Substitutes the PRO tag in verb forms with an enclitic or mesoclitic pronoun for tags representing the lemma and morpho-syntactic features of these pronouns. Thus, conversions like the following are performed:

degustares-lhe	degustar+V+PRO+INF+2+SG
degustares-lhe	degustar+V.ele.DAT.3.SG+SBJF+2+SG

The ambiguity of forms with the clitic pronoun "nos" is handled by means of the tag mapping CLITIC_MAPPING

nos	ele.ACC.3.M.PL/nós.AD.1.PL

Thus,an ambiguous entry like 

vindimam-nos	vindimar+V+PRO+PRS+3+PL

is split into two separate entries

vindimam-nos	vindimar+V.ele.ACC.3.M.PL+PRS+3+PL
vindimam-nos	vindimar+V.nós.AD.1.PL+PRS+3+PL

In forms with a non-ambiguous "nos", the clitic is mapped to AD.1.PL+PRS+3+PL. Thus, an entry like

vindicávei-nos	vindicar+V+PRO+IMPF+2+PL

is converted to

vindicávamo-nos vindicar+nós.AD.1.PL+IMPF+1+PL

    """
    # if clitic maps to "ele.ACC.3.M.PL/nós.AD.1.PL", then the length of cat_list is 2;
    # else, it is 1
    cat_list= AppendCliticFeatures(word,cat).split("/")
    # if the clitic has two feature sets, then the ambiguity of clitic "nos"
    # after nasal diphthong must be handled
    if len(cat_list)==2:
        # inserting category label into second list of features
        cat_list[1]="%s.%s" % (cat_list[0].split(".")[0],cat_list[1])
        # if this condition is true, then clitic has two readings;
        # else it only has the second reading
        if EndsInNasalDiphthong(word):
            # print word
            entries=[]
            for c in cat_list:
                entries.append("%s\t%s+%s+%s" % (word,lemma,c,ConcatenateFeatures(feats)))
            return "\n".join(entries)
        else:
            cat=cat_list[1]
    else:
            cat=cat_list[0]
    return "%s\t%s+%s+%s" % (word,lemma,cat,ConcatenateFeatures(feats))

def toString(word,lemma,cat,feats):
    return "%s\t%s+%s+%s" % (word,
                             lemma,
                             cat,
                             ConcatenateFeatures(feats))

def ConvertEntry(entry):
    parts=ParseEntry(entry)
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
    return toString(word,lemma,cat,ConvertFeatures(feats))

def ConvertEntriesFromFile(filename):
    entries=ExtractEntries(OpenFile(filename))
    return [ConvertEntry(e) for e in entries]
    
def WriteFile(entries,infile):
    f=open("%s.%s" % (infile,EXTENSION), "w")
    for e in entries:
        f.write("%s\n" % e.encode("utf-8"))
    f.close()

def main(): 
    for file in sys.argv[1:]:
        WriteFile(ConvertEntriesFromFile(file),file)

if __name__ == '__main__':
	main()
