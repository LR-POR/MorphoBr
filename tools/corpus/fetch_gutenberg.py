#!/usr/bin/env python3
"""Baixa livros do Projeto Gutenberg pelo espelho oficial (aleph.pglaf.org).

Uso: fetch_gutenberg.py DIRETORIO ID [ID ...]

Para escolher IDs em português: https://gutendex.com/books/?languages=pt
Grava DIRETORIO/<ID>.txt. Um livro por vez, com pausa entre eles.
"""
import os
import sys
import time
import urllib.error
import urllib.request

MIRROR = 'https://aleph.pglaf.org'
UA = {'User-Agent': 'MorphoBr-corpus/0.1 (lexicon coverage; low volume)'}


def path(book_id):
    # 55752 -> 5/5/7/5/55752/
    s = str(book_id)
    return '/'.join(s[:-1]) + '/' + s + '/'


def main():
    outdir, ids = sys.argv[1], sys.argv[2:]
    os.makedirs(outdir, exist_ok=True)
    for book_id in ids:
        for name in (f'{book_id}-0.txt', f'{book_id}-8.txt', f'{book_id}.txt'):
            url = f'{MIRROR}/{path(book_id)}{name}'
            try:
                req = urllib.request.Request(url, headers=UA)
                data = urllib.request.urlopen(req, timeout=60).read()
            except urllib.error.HTTPError:
                continue
            enc = 'latin-1' if name.endswith('-8.txt') else 'utf-8'
            with open(os.path.join(outdir, f'{book_id}.txt'), 'w', encoding='utf-8') as f:
                f.write(data.decode(enc, errors='replace'))
            print(book_id, name, file=sys.stderr)
            break
        else:
            print(book_id, 'não encontrado', file=sys.stderr)
        time.sleep(3)


if __name__ == '__main__':
    main()
