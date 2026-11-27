#!/usr/bin/env python3
"""Baixa o texto de artigos aleatórios da Wikipédia em português.

Uso: fetch_wiki.py N SAIDA.txt

Faz uma requisição por artigo, com pausa entre elas, para respeitar os limites
da API da Wikimedia. Os artigos ficam separados por duas linhas em branco.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = 'https://pt.wikipedia.org/w/api.php'
UA = {'User-Agent': 'MorphoBr-corpus/0.1 (lexicon coverage; low volume)'}
PAUSE = 2  # segundos entre requisições


def get(params):
    url = API + '?' + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    return None


def main():
    n, out = int(sys.argv[1]), sys.argv[2]
    r = get({'action': 'query', 'format': 'json', 'list': 'random',
             'rnnamespace': 0, 'rnlimit': min(n, 500)})
    titles = [x['title'] for x in r['query']['random']]
    got = 0
    with open(out, 'w', encoding='utf-8') as f:
        for t in titles:
            time.sleep(PAUSE)
            r = get({'action': 'query', 'format': 'json', 'prop': 'extracts',
                     'explaintext': 1, 'titles': t, 'formatversion': 2})
            text = r and r['query']['pages'][0].get('extract', '')
            if text:
                f.write(text + '\n\n\n')
                got += 1
    print(got, 'artigos', file=sys.stderr)


if __name__ == '__main__':
    main()
