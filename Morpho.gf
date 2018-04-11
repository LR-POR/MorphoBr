abstract Morpho = {
  cat S ; NF ; Gender ; Number ; Degree ; VF ;
      MT ; -- Mood + Tense
      Person ;
  fun
    mkN : String -> String -> NF -> S ;
    mkNF : Gender -> Number -> Degree -> NF ;
    Masc, Fem, Common, ZGender : Gender ;
    Sg, Pl, InvN, ZNumber : Number ;
    Dim, Aug, Super, ZDegree : Degree ;
    mkV : String -> String -> VF -> S ;
    mkVF : MT -> Person -> Number -> Gender -> VF ;
    Inf, Ger, PPart, Pres, Impf, Perf, Fut, Pqp, SPres, SImpf, SFut, Imp, Cond : MT ;
    P1, P2, P3, ZPerson: Person ;
} ;
