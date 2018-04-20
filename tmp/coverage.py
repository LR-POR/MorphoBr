#!/usr/bin/python3

import freeling
import sys

def load_wordlist(file):
    words = []
    with open(file, 'r') as f:
        words = [ x.split('\t')[0].strip() for x in f ]
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
for form in wordlist:
    w = freeling.word(form)
    dic.annotate_word(w)
    lemma = w.get_lemma()
    if not lemma:
        lemma = "_"
    print ("\t".join([form, str(w.found_in_dict()), lemma]))


