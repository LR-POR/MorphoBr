def parse_entry(e):
    [f,ts] = e.split("\t")
    l, *fs = ts.split("+")
    return (f,l,fs)

def enrich_clitic(ve):
    def clitic_tags(f):
        cmap = {"a":[".ele.ACC.3.F.SG"],"as":[".ele.ACC.3.F.PL"],"la":
                [".ele.ACC.3.F.SG"],"las":[".ele.ACC.3.F.PL"],"lhe":
                [".ele.DAT.3.SG"],"lhes":[".ele.DAT.3.PL"],"lo":
                [".ele.ACC.3.M.SG"],"los":[".ele.ACC.3.M.PL"],"me":
                [".eu.AD.1.SG"],"na":["ele.ACC.3.F.SG"],"nas":
                [".ele.ACC.3.F.PL"],"no":[".ele.ACC.3.M.SG"],"nos":
                [".ele.ACC.3.M.PL", ".nós.AD.1.PL"],
                "o":["ele.ACC.3.M.SG"],"os":[".ele.ACC.3.M.PL"],"se":
                [".ele.REFL"],"te":["tu.AD.2.SG"],"vos":[".vós.AD.2.PL"]}
        i = f.rfind("-")
        if i == -1:
            return [""]
        else:
            c = f[i+1:]
            return cmap[c]

    f, l, fs = ve
    cl, *fs = fs
    if cl == "V":
        return [(f, l, [(cl + cts)] + fs) for cts in clitic_tags(f)]
    else:
        return [ve]

def print_entry(pe):
    f, l, fs = pe
    return "{}\t{}".format(f, "+".join([l]+fs))

def read_dict(fp):
    with open(fp, mode='r', encoding="utf8") as fh:
        for l in fh:
            yield l

if __name__ == "__main__":
    from sys import argv
    ls = read_dict(argv[1])
    for l in ls:
        e = parse_entry(l)
        ee = enrich_clitic(e)
        list(map(lambda e: print(print_entry(e), end=''), ee))
