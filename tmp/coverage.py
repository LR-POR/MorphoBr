#!/usr/bin/python3

## TODO: make sure the wordform-lemma values in dictionary are UNIQUE!
## Alternative make the output of this program unique by running it via sort|uniq

import freeling
import sys

def get_form(x):
    return x.strip().split('\t')[0]

def get_lemma(x):
    return x.strip().split('\t')[1].split('+')[0]

def get_pos(x):
    return x.strip().split('\t')[1].split('+')[1]

def load_wordlist(file):
    words = []
    with open(file, 'r') as f:
        words = set([ (get_form(x), get_lemma(x)) for x in f ])
    return words

def is_pos(word_tag, pos_list):
    for pos in pos_list:
        if word_tag.startswith(pos):
            return True
    return False

wordlist = load_wordlist(sys.argv[1])
pos = sys.argv[2]

FREELINGDIR = "/usr/local";

DATA = FREELINGDIR+"/share/freeling/";
LANG="pt";

freeling.util_init_locale("default");

# dictionary(const std::wstring &Lang, const std::wstring &dicFile, 
#            const std::wstring &sufFile, const std::wstring &compFile,
#            bool invDic=false, bool retok=true);

dic = freeling.dictionary("pt", DATA+LANG+"/dicc.src",
                    DATA+LANG+"/afixos.dat",
                    "")

## Three possible outcomes:
## INDICT - wordform recognized direclty in Freeling's dictionary with the correct POS
## INRULES - wordform recognized indirectly via Freeling's rules with the correct POS
## MISSING - wordform not known to Freeling with the given POS
for (wform,wlemma) in wordlist:
    ww = freeling.word(wform)
    wl = freeling.word(wlemma)

    dic.annotate_word(ww)
    dic.annotate_word(wl)

    if wl.found_in_dict() and is_pos(wl.get_tag(), pos):
        flemma = ww.get_lemma()
        fpos = ww.get_tag()
        findict = ww.found_in_dict()

        status = "MISSING"
        if is_pos(fpos, pos):
            if findict:
                status = "IN-DICT"
            else:
                if flemma:
                    status = "IN-RULES"
                else:
                    flemma = "_"

        if not fpos:
            fpos = "_"
            
        print ("\t".join(["{}/{}".format(wform,wlemma), status, fpos[0], flemma, str(findict)]))
