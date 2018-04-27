concrete MorphoDel of Morpho = open Prelude, Predef in {
  lincat
    S = SS ; -- entry
    NF, VF, AF, AdvF = SS ; -- class features
    Gender, Number, Degree, Person, VT, AdvT = SS ; -- features
  lin
    ---
    -- features

    -- gender
    Masc = ss "m" ;
    Fem = ss "f" ;
    ZGender = ss nonExist ;
    Common = ss "" ;
    -- number
    Sg = ss "s" ;
    Pl = ss "p" ;
    InvN = ss "" ;
    ZNumber = ss nonExist ;
    -- degree
    Dim = ss "D" ;
    Aug = ss "A" ;
    Super = ss "S" ;
    ZDegree = ss "" ;
    -- person
    P1 = ss "1" ;
    P2 = ss "2" ;
    P3 = ss "3" ;
    ZPerson = ss "" ;
    -- V type
    Inf = ss "W" ;
    Ger = ss "G" ;
    PPart = ss "K" ;
    Pres = ss "P" ;
    Impf = ss "I" ;
    Perf = ss "J" ;
    Fut = ss "F" ;
    Pqp = ss "Q" ;
    SPres = ss "S" ;
    SImpf = ss "T" ;
    SFut = ss "U" ;
    Imp = ss "Y" ;
    Cond = ss "C" ;
    -- Adv type
    GAdv = ss "" ;
    NAdv = ss ":N" ;

    ---
    -- classes

    -- N
    mkN = mkEntry ;
    mkNF g n d = ss ("N" ++ ":" ++ d.s ++ g.s ++ n.s) ;
    -- V
    mkV = mkEntry ;
    mkVF mt p n g = ss ("V" ++ ":" ++ mt.s ++ p.s ++ g.s ++ n.s) ;
    -- A
    mkA = mkEntry ;
    mkAF d g n = ss ("A" ++ ":" ++ d.s ++ g.s ++ n.s) ;
    -- Adv
    mkAdv = mkEntry ;
    mkAdvF at = ss ("ADV" ++ strOpt ":" ++ at.s) ;

  oper
    mkEntry : SS -> SS -> SS -> SS ;
    mkEntry fo l fs = ss (fo.s ++ "," ++ l.s ++ "." ++ fs.s) ;
} ;
