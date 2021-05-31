# check-tools

Tools for checking the compatibility between a lexical resource and a treebank.

This module shows how to use unification to detect errors in a lexical
resource or treebank, comparing the two resources against one another.

Sketch of the algorithm:

TODO: create class UD_BosqueTreebank with method tagged_sents etc.
(e.g. subclass of nltk.corpus.CorpusReader)

TODO: create Python dictionary from MorphoBr, e.g.

morpho={'baratas':["barato+A+F+PL","barata+N+F+PL","baratar+V+PRS+2+SG"], ...}
treebank=UD_BosqueTreebank("pt_bosque-ud-*.conllu")
sentences=treebank.tagged_sents()

for sentence in sentences:
    for word,tag in sentence:
        token_fst=convert(tag,bosque) # e.g. convert("simples+ADJ+Gender=Fem|Number=Plur",bosque)
        entries=morphobr.get(word)
        if entries:
            errors=check(token_fst,[convert(e) for e in entries])
            if errors:
                pprint(errors)
        else:
            print "not found in dict"

Example sentence:

text = «É uma obra que fala de fé e eu espero que possibilite ao público uma compreensão direta do gospel, uma música de palavras simples e profundas.»
sent_id = CF733-3

27	palavras	palavra	NOUN	_	Gender=Fem|Number=Plur	25	nmod	_	_
28	simples	simples	ADJ	_	Gender=Masc|Number=Plur	27	amod	_	_

underspecified entry in MorphoBr


