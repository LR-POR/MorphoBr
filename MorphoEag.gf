concrete MorphoEag of Morpho = open Prelude, Predef in {
  lincat
    NF = SS ;
    S, Gender, Number, Degree, MT, Person = SS ;
  lin
    mkN  = mkEntry ;
    mkNF g n d = ss ("N" ++ ("C" | "P") ++ g.s ++ n.s ++ ("S" | "G" | "O" | "V" | "0") ++ "0" ++ d.s) ;
    Masc = ss "M" ;
    Fem = ss "F" ;
    Common = ss "C" ;
    ZGender = ss "0" ;
    Sg = ss "S" ;
    Pl = ss "P" ;
    InvN = ss "N" ;
    ZNumber = ss "0" ;
    Dim = ss "D" ;
    Aug = ss "A" ;
    Super = ss "S" ;
    ZDegree = ss "0" ;
    mkV = mkEntry ;
    mkVF mt p n g = ss ("V" ++ ("M" | "A" | "S") ++ mt.s ++ p.s ++ n.s ++ g.s) ;
    Inf = ss "N 0" ;
    Ger = ss "G 0" ;
    PPart = ss "P 0" ;
    Pres = ss "I P" ;
    Impf = ss "I I" ;
    Perf = ss "I S" ;
    Fut = ss "I F" ;
    Pqp = ss "I M" ;
    SPres = ss "S P" ;
    SImpf = ss "S I" ;
    SFut = ss "S F" ;
    Imp = ss "M 0" ;
    Cond = ss "I C" ;
    P1 = ss "1" ;
    P2 = ss "2" ;
    P3 = ss "3" ;
    ZPerson = ss "0" ;
  oper
    mkEntry : SS -> SS -> SS -> SS ;
    mkEntry fo l fs = ss (fo.s ++ l.s ++ fs.s) ;
} ;
