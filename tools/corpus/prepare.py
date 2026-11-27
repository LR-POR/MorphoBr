#!/usr/bin/env python3
"""Limpa textos, segmenta em sentenças e tokeniza.

Uso: prepare.py TIPO PREFIXO_SAIDA ARQUIVO [ARQUIVO ...]

TIPO é wiki (texto da API da Wikipédia), gutenberg (livros do Gutenberg) ou
plain (um parágrafo por bloco separado por linha em branco).

Gera PREFIXO_SAIDA.sents.txt (uma sentença por linha) e
PREFIXO_SAIDA.tokens.tsv (sentença, posição, token).

Usa só componentes do spaCy baseados em regras: o tokenizador de
spacy.blank('pt') e o sentencizer, que segmenta pela pontuação. Não usa
nenhum modelo treinado (etiquetador, lematizador ou parser), porque os
modelos para o português são treinados no Bosque/UD, cujas decisões podem
conflitar com as do MorphoBr (ver docs/principles.md, seção 5).
"""
import re
import sys

import spacy

STOP_SECTIONS = re.compile(
    r'^=+\s*(Referências|Ligações externas|Bibliografia|Ver também|Notas|'
    r'Fontes|Leitura adicional|Notas e referências)\s*=+\s*$', re.I)


def clean_wiki(text):
    paras = []
    for article in text.split('\n\n\n'):
        skip = False
        for line in article.split('\n'):
            line = line.strip()
            if STOP_SECTIONS.match(line):
                skip = True
                continue
            if re.match(r'^=+.*=+$', line):  # título de seção
                skip = False
                continue
            if line and not skip:
                paras.append(line)
    return paras


def clean_gutenberg(text):
    start = re.search(r'\*\*\* ?START OF.*?\*\*\*', text)
    end = re.search(r'\*\*\* ?END OF', text)
    text = text[start.end() if start else 0:end.start() if end else len(text)]
    paras = []
    for p in re.split(r'\n\s*\n', text.replace('\r', '')):
        p = re.sub(r'\[[^\]]*\]', '', p)       # notas: [Ilustração], [Pg 12]
        p = p.replace('_', '')                 # itálico: _palavra_
        p = re.sub(r'\s*\n\s*', ' ', p).strip()  # junta as linhas do parágrafo
        if len(p) < 2 or re.fullmatch(r'[IVXLC\d\s.\-—*]+', p):  # numeração
            continue
        paras.append(p)
    return paras


def clean_plain(text):
    return [re.sub(r'\s+', ' ', p).strip()
            for p in re.split(r'\n\s*\n', text) if p.strip()]


CLEANERS = {'wiki': clean_wiki, 'gutenberg': clean_gutenberg, 'plain': clean_plain}


def main():
    kind, prefix, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    paras = []
    for f in files:
        with open(f, encoding='utf-8', errors='replace') as fh:
            paras += CLEANERS[kind](fh.read())
    nlp = spacy.blank('pt')
    nlp.add_pipe('sentencizer')
    nlp.max_length = 2_000_000
    n = 0
    with open(prefix + '.sents.txt', 'w', encoding='utf-8') as sents, \
         open(prefix + '.tokens.tsv', 'w', encoding='utf-8') as toks:
        for doc in nlp.pipe(paras, batch_size=64):
            for s in doc.sents:
                n += 1
                sents.write(s.text.strip() + '\n')
                for i, t in enumerate(s):
                    toks.write(f'{n}\t{i}\t{t.text}\n')
    print(f'{len(paras)} parágrafos, {n} sentenças', file=sys.stderr)


if __name__ == '__main__':
    main()
