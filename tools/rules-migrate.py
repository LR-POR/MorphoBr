#!/usr/bin/env python3
"""Move para as regras (rules/ + lexicon/) os pares que elas reproduzem.

Estratégia mista (ver #143): um lema ainda listado por extenso em verbs/*.dict
é testado com a classe de flexão proposta para ele (pela terminação, ver
CLASSES). Ele passa no critério se as regras não gerarem nenhum par que não
esteja no dicionário (gerado ⊆ dicionário). Para os lemas que passam:

  - o lema é acrescentado a lexicon/verbs/<modelo>.tsv;
  - os pares gerados são removidos de verbs/*.dict; o que sobra (variantes,
    formas irregulares, homógrafos) continua full-form.

Assim, regras ∪ full-form restante = exatamente o léxico anterior. O script é
idempotente: rodá-lo de novo depois de acrescentar uma classe migra mais lemas.

Uso: tools/rules-migrate.py [--dry-run]
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

# Classe proposta para cada lema, pela terminação (a primeira que casar).
# A atribuição só é aceita se o lema passar no critério.
CLASSES = [("ear", "passear"), ("ar", "abafar")]


def read_dicts():
    pairs = collections.defaultdict(set)
    for fn in sorted(glob.glob(os.path.join(ROOT, "verbs", "*.dict"))):
        with open(fn, encoding="utf-8") as fh:
            for line in fh:
                form, ana = line.rstrip("\n").split("\t")
                pairs[ana.split("+")[0]].add((form, ana))
    return pairs


def read_lexicon():
    lex = {}
    for fn in glob.glob(os.path.join(ROOT, "lexicon", "verbs", "*.tsv")):
        model = os.path.basename(fn)[:-4]
        with open(fn, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    lex[line.strip()] = model
    return lex


def write_lexicon(lex, lexdir):
    by_model = collections.defaultdict(list)
    for lemma, model in lex.items():
        by_model[model].append(lemma)
    os.makedirs(lexdir, exist_ok=True)
    for model in {m for _, m in CLASSES} | set(by_model):
        lemmas = sorted(by_model.get(model, []), key=lambda s: s.encode("utf-8"))
        with open(os.path.join(lexdir, model + ".tsv"), "w", encoding="utf-8") as fh:
            fh.writelines(l + "\n" for l in lemmas)


def generate(lex):
    """Pares (forma, análise) gerados pelas regras para os lemas em lex."""
    with tempfile.TemporaryDirectory() as tmp:
        write_lexicon(lex, os.path.join(tmp, "lexicon", "verbs"))
        os.symlink(os.path.join(ROOT, "rules"), os.path.join(tmp, "rules"))
        os.makedirs(os.path.join(tmp, "tools"))
        os.symlink(os.path.join(ROOT, "tools", "lexicon-to-lexc.sh"),
                   os.path.join(tmp, "tools", "lexicon-to-lexc.sh"))
        # o script resolve rules/ e lexicon/ relativos a si mesmo: pelo link
        # em tmp/tools, usa as regras do repositório e o léxico temporário
        lexc = subprocess.run([os.path.join(tmp, "tools", "lexicon-to-lexc.sh")],
                              check=True, capture_output=True, text=True).stdout
        with open(os.path.join(tmp, "verbs.lexc"), "w", encoding="utf-8") as fh:
            fh.write(lexc)
        script = (f"read lexc {tmp}/verbs.lexc\ndefine Lex ;\n"
                  f"source {ROOT}/rules/orthography.foma\n"
                  f"regex Lex .o. Orthography ;\nprint pairs > {tmp}/pairs.txt\n")
        with open(os.path.join(tmp, "gen.foma"), "w", encoding="utf-8") as fh:
            fh.write(script)
        subprocess.run([FOMA, "-f", os.path.join(tmp, "gen.foma")], check=True,
                       capture_output=True)
        gen = collections.defaultdict(set)
        with open(os.path.join(tmp, "pairs.txt"), encoding="utf-8") as fh:
            for line in fh:
                ana, form = line.rstrip("\n").split("\t")
                gen[ana.split("+")[0]].add((form, ana))
        return gen


def main():
    dry = "--dry-run" in sys.argv
    dic = read_dicts()
    lex = read_lexicon()

    # 1. propõe uma classe para cada lema ainda não migrado e testa o critério
    cand = {}
    for lemma in dic:
        if lemma in lex:
            continue
        for suffix, model in CLASSES:
            if lemma.endswith(suffix):
                cand[lemma] = model
                break
    gen = generate(cand)
    passed = {l: m for l, m in cand.items() if gen[l] and gen[l] <= dic[l]}
    failed = len(cand) - len(passed)
    print(f"candidatos: {len(cand)}  passam: {len(passed)}  não passam: {failed}")

    # 2. confere com o léxico completo (já migrados + novos)
    new_lex = {**lex, **passed}
    gen = generate(new_lex)
    for lemma in passed:
        assert gen[lemma] <= dic[lemma], lemma
    remove = set().union(*(gen[l] for l in passed)) if passed else set()
    print(f"pares a remover de verbs/*.dict: {len(remove)}")
    if dry:
        return

    # 3. grava o léxico e remove dos .dict os pares gerados
    write_lexicon(new_lex, os.path.join(ROOT, "lexicon", "verbs"))
    for fn in sorted(glob.glob(os.path.join(ROOT, "verbs", "*.dict"))):
        with open(fn, encoding="utf-8") as fh:
            lines = fh.readlines()
        out = [l for l in lines if tuple(l.rstrip("\n").split("\t")) not in remove]
        if len(out) != len(lines):
            with open(fn, "w", encoding="utf-8") as fh:
                fh.writelines(out)


if __name__ == "__main__":
    main()
