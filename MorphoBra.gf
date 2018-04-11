concrete MorphoBra of Morpho = open Prelude, Predef in {
  lincat
    NF = SS ;
    S, Gender, Number, Degree = SS ;
  lin
    mkN f l nf  = ss (f.s ++ "\t" ++ l.s ++ nf.s) ;
    mkNF g n d = ss ("N" ++ d.s ++ g.s ++ n.s) ;
    Masc = ss "+M" ;
    Fem = ss "+F" ;
    Common = ss ("+M" | "+F") ;
    Sg = ss "+S" ;
    Pl = ss "+P" ;
    Dim = ss "+D" ;
    Aug = ss "+A" ;
    Super = ss "+S" ;
    ZDegree = ss "" ;

} ;