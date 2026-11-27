#!/usr/bin/env python3
"""Mede a cobertura do MorphoBr sobre tokens de um corpus e classifica as
palavras sem análise.

Uso: coverage.py MORPHOBR_BIN TOKENS.tsv [TOKENS.tsv ...] [--oov SAIDA.tsv]

TOKENS.tsv vem de prepare.py. O flookup é procurado na variável FLOOKUP ou no
PATH. Para cada arquivo, imprime um relatório; com --oov, grava as palavras
sem análise (arquivo, categoria, palavra, frequência).

Excluídos da contagem:
- palavras de classe fechada (closed_class.txt), que o MorphoBr ainda não
  cobre (#191);
- nomes próprios: palavras com maiúscula que nunca aparecem em minúscula no
  mesmo arquivo;
- símbolos, abreviaturas, números e números romanos.

Categorias das palavras sem análise:
- hífen: clítico / hífen: composto;
- grafia antiga: a forma passa a ter análise depois de normalizações como
  ll -> l, ph -> f, ct -> t, ou sem o acento (elle, fallar, sophá, póde);
- provável estrangeirismo: só letras ASCII, com th, sh, w, k, y, ck, oo, ee;
- outras: candidatas a palavras que faltam, para conferir à mão.
"""
import collections
import itertools
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLIT = r'(me|te|se|nos|vos|lhe|lhes|o|a|os|as|lo|la|los|las|no|na|nas|mo|ma|lho|lha)'
WORD = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*")
OLD_RULES = [('ph', 'f'), ('th', 't'), ('y', 'i'), ('ll', 'l'), ('mm', 'm'),
             ('nn', 'n'), ('tt', 't'), ('pp', 'p'), ('ff', 'f'), ('gg', 'g'),
             ('cc', 'c'), ('ct', 't'), ('pt', 't'), ('mn', 'n'), ('ahi', 'aí'),
             ('ae$', 'ai'), ('ao$', 'au'), ('z$', 's'), ('^h', '')]
NO_ACCENTS = str.maketrans('áéíóúêô', 'aeioueo')


def old_variants(w):
    v = {w}
    for a, b in OLD_RULES:
        v |= {re.sub(a, b, x) for x in v}
    v |= {x.translate(NO_ACCENTS) for x in v}
    return v - {w}


def lookup(binfile, words):
    flookup = os.environ.get('FLOOKUP') or shutil.which('flookup')
    if not flookup:
        sys.exit('flookup não encontrado: defina FLOOKUP ou ponha no PATH')
    out = subprocess.run([flookup, '-i', binfile], input='\n'.join(words) + '\n',
                         capture_output=True, text=True, check=True).stdout
    known = set()
    for line in out.split('\n'):
        p = line.split('\t')
        if len(p) == 2 and p[1] != '+?':
            known.add(p[0])
    return known


def read_tokens(path):
    toks = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 3 and re.search(r'[^\W\d_]', p[2]):
                toks.append(p[2])
    return toks


def main():
    args = sys.argv[1:]
    oov_out = None
    if '--oov' in args:
        i = args.index('--oov')
        oov_out = args[i + 1]
        del args[i:i + 2]
    binfile, files = args[0], args[1:]
    with open(os.path.join(HERE, 'closed_class.txt'), encoding='utf-8') as f:
        closed = {l.strip() for l in f if l.strip() and not l.startswith('#')}

    data = {f: read_tokens(f) for f in files}
    types = {x for toks in data.values() for w in toks for x in (w, w.lower())}
    variants = {w: old_variants(w.lower()) for w in types}
    known = lookup(binfile, sorted(types | set(itertools.chain.from_iterable(variants.values()))))

    rows = []
    for f, toks in data.items():
        lowers = {w for w in toks if w == w.lower()}
        cnt = collections.Counter()
        oov = collections.defaultdict(collections.Counter)
        for w in toks:
            lw = w.lower()
            if lw in closed:
                cnt['classe fechada, ainda não coberta (#191)'] += 1
                continue
            if w != lw and lw not in lowers:
                cnt['nome próprio'] += 1
                continue
            if (len(w) == 1 or re.fullmatch(r'[ivxlcdm]+', lw)
                    or not WORD.fullmatch(w)):
                cnt['símbolo/abreviatura/romano'] += 1
                continue
            cnt['avaliados'] += 1
            if w in known or lw in known:
                cnt['com análise'] += 1
                continue
            if '-' in w:
                k = ('hífen: clítico' if re.search('-' + CLIT + '(-|$)', lw)
                     else 'hífen: composto')
            elif any(x in known for x in variants.get(w, ())):
                k = 'grafia antiga'
            elif re.fullmatch(r'[a-z]+', lw) and re.search(r'th|sh|w|k|y|ck|oo|ee', lw):
                k = 'provável estrangeirismo'
            else:
                k = 'outras'
            oov[k][lw] += 1
        ev = cnt['avaliados'] or 1
        print(f'== {f}: {len(toks)} tokens alfabéticos')
        for k in ('classe fechada, ainda não coberta (#191)', 'nome próprio', 'símbolo/abreviatura/romano'):
            print(f'   excluídos ({k}): {cnt[k]}')
        print(f'   avaliados: {cnt["avaliados"]}; com análise: {cnt["com análise"]} '
              f'({100 * cnt["com análise"] / ev:.1f}%)')
        for k, v in sorted(oov.items(), key=lambda x: -sum(x[1].values())):
            print(f'   sem análise ({k}): {len(v)} tipos, {sum(v.values())} ocorrências')
            rows += [(f, k, w, n) for w, n in v.most_common()]
    if oov_out:
        with open(oov_out, 'w', encoding='utf-8') as fh:
            for r in rows:
                fh.write('\t'.join(map(str, r)) + '\n')


if __name__ == '__main__':
    main()
