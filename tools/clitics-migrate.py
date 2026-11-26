#!/usr/bin/env python3
"""Move para as regras de clíticos (rules/clitics.foma) os pares que elas
reproduzem (estratégia mista, ver #143 e #165).

Um lema de clitics/*.dict passa no critério se as regras gerarem algum par
para ele e todos os pares gerados estiverem no dicionário (gerado ⊆
dicionário). Para os lemas que passam:

  - o lema é acrescentado a lexicon/clitics/verbs.tsv;
  - os pares gerados são removidos de clitics/*.dict; o que sobra (células e
    variantes que as regras não cobrem) continua full-form.

Assim, regras ∪ full-form restante = exatamente o léxico anterior. O script é
idempotente: rodá-lo de novo depois de mudar as regras ou os dados migra mais
lemas.

Uso: tools/clitics-migrate.py [--dry-run]
Variável FOMA: caminho do foma (padrão: foma no PATH).
"""

import collections
import glob
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEXICON = os.path.join(ROOT, "lexicon", "clitics", "verbs.tsv")


def lemma_of(ana):
    return ana.split("+", 1)[0]


def read_dicts():
    pairs = collections.defaultdict(set)
    for fn in sorted(glob.glob(os.path.join(ROOT, "clitics", "*.dict"))):
        with open(fn, encoding="utf-8") as fh:
            for line in fh:
                form, ana = line.rstrip("\n").split("\t")
                pairs[lemma_of(ana)].add((form, ana))
    return pairs


def read_lexicon():
    if not os.path.exists(LEXICON):
        return set()
    with open(LEXICON, encoding="utf-8") as fh:
        return {l.strip() for l in fh if l.strip()}


def write_lemmas(lemmas, fn):
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, "w", encoding="utf-8") as fh:
        fh.writelines(l + "\n" for l in sorted(lemmas, key=lambda s: s.encode("utf-8")))


def generate(lemmas):
    """Pares (forma, análise) gerados pelas regras para os lemas dados."""
    with tempfile.TemporaryDirectory() as tmp:
        fn = os.path.join(tmp, "lemmas.tsv")
        write_lemmas(lemmas, fn)
        out = subprocess.run([os.path.join(ROOT, "tools", "clitics.sh"), fn],
                             check=True, capture_output=True, text=True).stdout
    gen = collections.defaultdict(set)
    for line in out.splitlines():
        form, ana = line.split("\t")
        gen[lemma_of(ana)].add((form, ana))
    return gen


def main():
    dry = "--dry-run" in sys.argv
    dic = read_dicts()
    lex = read_lexicon()

    cand = [l for l in dic if l not in lex]
    gen = generate(cand)
    passed = {l for l in cand if gen[l] and gen[l] <= dic[l]}
    print(f"candidatos: {len(cand)}  passam: {len(passed)}  não passam: {len(cand) - len(passed)}")
    ident = sum(1 for l in passed if gen[l] == dic[l])
    print(f"  idênticos (o lema sai de clitics/*.dict): {ident}")

    # confere com o léxico completo (já migrados + novos)
    new_lex = lex | passed
    gen = generate(new_lex)
    for lemma in passed:
        assert gen[lemma] <= dic[lemma], lemma
    remove = set().union(*(gen[l] for l in passed)) if passed else set()
    total = sum(len(s) for s in dic.values())
    print(f"pares a remover de clitics/*.dict: {len(remove)} de {total}")
    if dry:
        return

    write_lemmas(new_lex, LEXICON)
    for fn in sorted(glob.glob(os.path.join(ROOT, "clitics", "*.dict"))):
        with open(fn, encoding="utf-8") as fh:
            lines = fh.readlines()
        out = [l for l in lines if tuple(l.rstrip("\n").split("\t")) not in remove]
        if len(out) != len(lines):
            with open(fn, "w", encoding="utf-8") as fh:
                fh.writelines(out)


if __name__ == "__main__":
    main()
