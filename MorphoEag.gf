concrete MorphoEag of Morpho = open Prelude, Predef in {
  lincat
    NF = SS ;
    S, Gender, Number, Degree = SS ;
  lin
    mkN f l nf  = ss (f.s ++ l.s ++ nf.s) ;
    mkNF g n d = ss ("N" ++ ("C" | "P") ++ g.s ++ n.s ++ ("S" | "G" | "O" | "V" | "0") ++ "0" ++ d.s) ;
    Masc = ss "M" ;
    Fem = ss "F" ;
    Common = ss "C" ;
    Sg = ss "S" ;
    Pl = ss "P" ;
    Dim = ss "D" ;
    Aug = ss "A" ;
    Super = ss "S" ;
    ZDegree = ss "0" ;

} ;