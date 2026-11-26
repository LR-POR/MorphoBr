#!/usr/bin/env python3
"""Cria uma classe de flexão verbal a partir das formas do verbo-modelo.

Lê em verbs/*.dict todas as análises do modelo (o modelo precisa ainda estar
listado por extenso), separa o radical (o modelo sem a terminação) e acrescenta:

  - a rules/verbs.lexc um LEXICON <MODELO> com uma entrada por análise
    (terminação+análise : fronteira + sufixo);
  - a rules/classes.tsv a linha modelo, terminação, sufixo de aplicação e
    fronteira.

A classe só é usada por tools/rules-migrate.py, que move para ela apenas os
lemas que passam no critério da estratégia mista (ver #143); por isso uma
classe nova nunca altera o conteúdo do léxico.

Uso: tools/make-class.py MODELO TERMINAÇÃO [APLICA-SE-A] [FRONTEIRA]
     ex.: tools/make-class.py aderir erir      (aplica-se a -erir, fronteira ^N)
"""

import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    model, ending = sys.argv[1], sys.argv[2]
    applies = sys.argv[3] if len(sys.argv) > 3 else ending
    boundary = sys.argv[4] if len(sys.argv) > 4 else "^N"
    if not model.endswith(ending) or not model.endswith(applies):
        sys.exit(f"{model} não termina em {ending}/{applies}")
    stem = model[: len(model) - len(ending)]

    classes = os.path.join(ROOT, "rules", "classes.tsv")
    with open(classes, encoding="utf-8") as fh:
        if any(l.split("\t")[0] == model for l in fh if not l.startswith("#")):
            sys.exit(f"a classe {model} já existe")

    rows = set()
    for fn in glob.glob(os.path.join(ROOT, "verbs", "*.dict")):
        with open(fn, encoding="utf-8") as fh:
            for line in fh:
                form, ana = line.rstrip("\n").split("\t")
                if ana.startswith(model + "+V+"):
                    if not form.startswith(stem):
                        sys.exit(f"forma {form} não começa pelo radical {stem}")
                    rows.add((ana[len(model) + 3:], form[len(stem):]))
    if not rows:
        sys.exit(f"{model} não está em verbs/*.dict")

    def esc(s):
        return "".join("%" + c if c in '%!;:<>"#0 -' else c for c in s)

    lexc = os.path.join(ROOT, "rules", "verbs.lexc")
    with open(lexc, encoding="utf-8") as fh:
        text = fh.read()
    multichar = next(l for l in text.split("\n") if l.startswith("Multichar_Symbols"))
    if boundary not in multichar.split():
        sys.exit(f"fronteira {boundary} não está em Multichar_Symbols")
    block = [f"", f"! Modelo: {model} (terminação -{ending}; aplica-se a -{applies}).",
             f"LEXICON {model.upper()}"]
    block += [f"{esc(ending)}+V+{tag}:{boundary}{esc(suf)} # ;" for tag, suf in sorted(rows)]
    with open(lexc, "a", encoding="utf-8") as fh:
        fh.write("\n".join(block) + "\n")
    with open(classes, "a", encoding="utf-8") as fh:
        fh.write(f"{model}\t{ending}\t{applies}\t{boundary}\n")
    print(f"classe {model.upper()}: {len(rows)} entradas")


if __name__ == "__main__":
    main()
