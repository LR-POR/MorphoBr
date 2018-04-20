#!/usr/bin/python3

import freeling
import sys

def get_form(x):
    return x.strip().split('\t')[0]

def get_lemma(x):
    return x.strip().split('\t')[1].split('+')[0]

def load_wordlist(file):
    words = []
    with open(file, 'r') as f:
        words = [ (get_form(x), get_lemma(x)) for x in f ]
    return words

wordlist = load_wordlist(sys.argv[1])

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
for (wform,wlemma) in wordlist:
    ww = freeling.word(wform)
    wl = freeling.word(wlemma)
    dic.annotate_word(ww)
    dic.annotate_word(wl)
    if wl.found_in_dict():
        lemma = ww.get_lemma()
        if not lemma:
            lemma = "_"
        print ("\t".join(["{}/{}".format(wform,wlemma), str(ww.found_in_dict()), lemma]))


