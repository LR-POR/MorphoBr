concrete MorphoBra of Morpho = open Prelude, Predef in {
  lincat
    S = SS ; -- entry
    NF, VF, AF, AdvF = SS ; -- class features
    Gender, Number, Degree, Person, VT, AdvT = SS ; -- features
  lin
    ---
    -- features

    -- gender
    Masc = ss "+M" ;
    Fem = ss "+F" ;
    ZGender = ss "" ;
    Common = Masc | Fem ;
    -- number
    Sg = ss "+SG" ;
    Pl = ss "+PL" ;
    InvN = Sg | Pl ;
    ZNumber = ss "" ;
    -- degree
    Dim = ss "+DIM" ;
    Aug = ss "+AUG" ;
    Super = ss "+SUPER" ;
    ZDegree = ss "" ;
    -- person
    P1 = ss "+1" ;
    P2 = ss "+2" ;
    P3 = ss "+3" ;
    ZPerson = ss "" ;
    -- V type
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
    -- Adv type
    GAdv = ss "" ;
    NAdv = ss "+NEG" ;

    ---
    -- classes

    -- N
    mkN = mkEntry ;
    mkNF g n d = ss ("+N" ++ d.s ++ g.s ++ n.s) ;
    -- V
    mkV = mkEntry ;
    mkVF mt p n g = ss ("+V" ++ mt.s ++ p.s ++ g.s ++ n.s) ;
    -- A
    mkA = mkEntry ;
    mkAF d g n = ss ("+A" ++ d.s ++ g.s ++ n.s) ;
    -- Adv
    mkAdv = mkEntry ;
    mkAdvF at = ss ("+ADV" ++ at.s) ;

  oper
    mkEntry : SS -> SS -> SS -> SS ;
    mkEntry fo l fs = ss (fo.s ++ "\t" ++ l.s ++ fs.s) ;
} ;
