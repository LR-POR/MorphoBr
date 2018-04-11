concrete MorphoBra of Morpho = open Prelude, Predef in {
  lincat
    S = SS ;
    NF, VF = SS ;
    Gender, Number, Degree, Mood, Tense, Person = SS ;
  lin
    mkN = mkEntry ;
    mkNF g n d = ss ("+N" ++ d.s ++ g.s ++ n.s) ;
    Masc = ss "+M" ;
    Fem = ss "+F" ;
    Common = ss ("+M" | "+F") ;
    Sg = ss "+S" ;
    Pl = ss "+P" ;
    Dim = ss "+DIM" ;
    Aug = ss "+AUG" ;
    Super = ss "+SUPER" ;
    ZDegree = ss "" ;
    mkV = mkEntry ;
    mkVF m t p n g = ss ("+V" ++ ("M" | "A" | "S") ++ (tense m.s t.s) ++ p.s ++ g.s ++ n.s) ;
    ZTense = ss "" ;
    ZPerson = ss "" ;
    ZNumber = ss "" ;
    Cond = ss "COND" ;
       Warning: no linearization of Cond
   Warning: no linearization of Fut
   Warning: no linearization of Ger
   Warning: no linearization of Imper
   Warning: no linearization of Imperf
   Warning: no linearization of Ind
   Warning: no linearization of Inf
   Warning: no linearization of P1
   Warning: no linearization of P2
   Warning: no linearization of P3
   Warning: no linearization of Part
   Warning: no linearization of Past
   Warning: no linearization of PlusQP
   Warning: no linearization of Pres
   Warning: no linearization of Sub

  oper
    mkEntry : SS -> SS -> SS -> SS ;
    mkEntry fo l fs = ss (fo.s ++ "\t" ++ l.s ++ fs.s) ;

    tense : Str -> Str -> Str ;
    tense m t = case <m,t> of {
      <"N","0"> => "+INF" ;
      <"G","0"> => "+GRD" ;
      <"P","0"> => "+PTPASS" ;
      <"M","0"> => "+IMP" ;
      <"S","F"> => "+SBJF" ;
      <"S","I"> => "+SBJP" ;
      <"S","P"> => "+SBJR" ;
      <"I","C"> => "+COND" ;
      <"I","F"> => "+FUT" ;
      <"I","I"> => "+IMPF" ;
      <"I","M"> => "+PQP" ;
      <"I","P"> => "+PRS" ;
      <"I","S"> => "+PRF" ;
      <_,_> =>
      } ;
} ;