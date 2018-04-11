concrete MorphoBra of Morpho = open Prelude, Predef in {
  lincat
    S = SS ;
    NF, VF = SS ;
    Gender, Number, Degree, MT, Person = SS ;
  lin
    mkN = mkEntry ;
    mkNF g n d = ss ("+N" ++ d.s ++ g.s ++ n.s) ;
    Masc = ss "+M" ;
    Fem = ss "+F" ;
    ZGender = ss "" ;
    Common = ss ("+M" | "+F") ;
    Sg = ss "+S" ;
    Pl = ss "+P" ;
    InvN = ss ("+S" | "+P") ;
    ZNumber = ss "" ;
    Dim = ss "+DIM" ;
    Aug = ss "+AUG" ;
    Super = ss "+SUPER" ;
    ZDegree = ss "" ;
    mkV = mkEntry ;
    mkVF mt p n g = ss ("+V" ++ mt.s ++ p.s ++ g.s ++ n.s) ;
    Inf = ss "+INF" ;
    Ger = ss "+GRD" ;
    PPart = ss "+PTPASS" ;
    Pres = ss "+PRF" ;
    Impf = ss "+IMPF" ;
    Perf = ss "+PRF" ;
    Fut = ss "+FUT" ;
    Pqp = ss "+PQP" ;
    SPres = ss "+SBJR" ;
    SImpf = ss "+SBJP" ;
    SFut = ss "+SBJF" ;
    Imp = ss "+IMP" ;
    Cond = ss "+COND" ;
    P1 = ss "+1" ;
    P2 = ss "+2" ;
    P3 = ss "+3" ;
    ZPerson = ss "" ;
  oper
    mkEntry : SS -> SS -> SS -> SS ;
    mkEntry fo l fs = ss (fo.s ++ "\t" ++ l.s ++ fs.s) ;
} ;
