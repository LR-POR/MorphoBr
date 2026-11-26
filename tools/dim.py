#!/usr/bin/env python3
"""Diminutivos e aumentativos+diminutivos gerados por regras (ver #149, #143).

A gramática de estados finitos de Leonel de Alencar (rules/dim/) gera os
diminutivos em -inho/-zinho a partir das bases (formas sem +DIM) de
substantivos e adjetivos dos arquivos .dict. lexicon/dim/nouns.tsv e
lexicon/dim/adjectives.tsv listam os lemas cujos diminutivos vêm das regras.

Subcomandos:
  generate         escreve na saída padrão os pares (forma<TAB>análise) gerados
                   para os lemas listados em lexicon/dim/, em ordem canônica;
  migrate [--dry-run]
                   estratégia mista: para cada lema (por categoria) com
                   diminutivos ainda listados nos .dict, testa se as regras não
                   geram nenhum par que não esteja no dicionário; se passar, o
                   lema entra em lexicon/dim/ e os pares gerados saem dos .dict.

Quando as formas masculina e feminina de um diminutivo coincidem, as duas
análises viram uma só, sem gênero (artistinha artista+N+DIM+SG), como no resto
do MorphoBr.

Variável FOMA: caminho do foma (padrão: foma no PATH).
"""

import collections
import glob
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOMA = os.environ.get("FOMA", "foma")
sys.path.insert(0, os.path.join(ROOT, "rules", "dim"))
import extract_bases  # noqa: E402

CATS = {"N": "nouns", "A": "adjectives"}
GRAMMAR = ["alternation-rules.xfst", "morphotactic-grammar.lexc", "compile-final-fst.xfst"]


def dict_lines():
    for cat, d in CATS.items():
        for fn in sorted(glob.glob(os.path.join(ROOT, d, "*.dict"))):
            with open(fn, encoding="utf-8") as fh:
                yield from fh


def read_lists():
    allowed = set()
    for cat, d in CATS.items():
        fn = os.path.join(ROOT, "lexicon", "dim", d + ".tsv")
        if os.path.exists(fn):
            with open(fn, encoding="utf-8") as fh:
                allowed |= {(l.strip(), cat) for l in fh if l.strip()}
    return allowed


def collapse(pairs):
    """Junta em uma análise sem gênero as formas iguais no masculino e no feminino."""
    groups = collections.defaultdict(set)
    for form, ana in pairs:
        p = ana.split("+")
        g = "M" if "M" in p else "F" if "F" in p else None
        groups[(form, "+".join(x for x in p if x not in ("M", "F")))].add((g, ana))
    out = set()
    for (form, neutral), v in groups.items():
        if {"M", "F"} <= {g for g, _ in v}:
            out.add((form, neutral))
        else:
            out |= {(form, ana) for _, ana in v}
    return out


def generate(allowed):
    """Pares (forma, análise) de diminutivos para os (lema, categoria) em allowed."""
    if not allowed:
        return set()
    with tempfile.TemporaryDirectory() as tmp:
        extract_bases.extract(dict_lines(), tmp, allowed)
        for name in GRAMMAR:
            os.symlink(os.path.join(ROOT, "rules", "dim", name), os.path.join(tmp, name))
        with open(os.path.join(tmp, "gen.foma"), "w", encoding="utf-8") as fh:
            fh.write("source compile-final-fst.xfst\nprint pairs > pairs.txt\n")
        r = subprocess.run([FOMA, "-f", "gen.foma"], cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(os.path.join(tmp, "pairs.txt")):
            sys.exit(r.stdout + r.stderr)
        pairs = set()
        with open(os.path.join(tmp, "pairs.txt"), encoding="utf-8") as fh:
            for line in fh:
                ana, form = line.rstrip("\n").split("\t")
                # arquivos de base vazios (listas pequenas) fazem a gramática
                # gerar sufixos soltos, sem lema (zinho +DIM+M+SG): descartados
                if not ana.startswith("+"):
                    pairs.add((form, ana))
    return collapse(pairs)


def canonical(pairs):
    return sorted(pairs, key=lambda p: (p[1].encode("utf-8"), p[0].encode("utf-8")))


def migrate(dry):
    allowed = read_lists()
    dims = collections.defaultdict(set)
    for line in dict_lines():
        form, ana = line.rstrip("\n").split("\t")
        p = ana.split("+")
        if "DIM" in p:
            dims[(p[0], p[1])].add((form, ana))
    cand = {k for k in dims if k not in allowed}
    gen = collections.defaultdict(set)
    for form, ana in generate(cand):
        p = ana.split("+")
        gen[(p[0], p[1])].add((form, ana))
    passed = {k for k in cand if gen[k] and gen[k] <= dims[k]}
    remove = set().union(*(gen[k] for k in passed)) if passed else set()
    print(f"candidatos: {len(cand)}  passam: {len(passed)}  não passam: {len(cand) - len(passed)}")
    print(f"pares a remover dos .dict: {len(remove)}")
    if dry:
        return
    os.makedirs(os.path.join(ROOT, "lexicon", "dim"), exist_ok=True)
    for cat, d in CATS.items():
        lemmas = sorted({l for l, c in allowed | passed if c == cat}, key=lambda s: s.encode("utf-8"))
        with open(os.path.join(ROOT, "lexicon", "dim", d + ".tsv"), "w", encoding="utf-8") as fh:
            fh.writelines(l + "\n" for l in lemmas)
        for fn in sorted(glob.glob(os.path.join(ROOT, d, "*.dict"))):
            with open(fn, encoding="utf-8") as fh:
                lines = fh.readlines()
            out = [l for l in lines if tuple(l.rstrip("\n").split("\t")) not in remove]
            if len(out) != len(lines):
                with open(fn, "w", encoding="utf-8") as fh:
                    fh.writelines(out)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "generate":
        for form, ana in canonical(generate(read_lists())):
            sys.stdout.write(f"{form}\t{ana}\n")
    elif cmd == "migrate":
        migrate("--dry-run" in sys.argv)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
