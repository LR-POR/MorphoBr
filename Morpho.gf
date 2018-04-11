abstract Morpho = {
  cat S ; -- entry
      NF ; VF ; AF ; -- class features
      -- features
      Gender ; Number ; Degree ;
      MT ; -- Mood + Tense
      Person ;
  fun
    ---
    -- features
    Masc, Fem, Common, ZGender : Gender ; -- gender
    Sg, Pl, InvN, ZNumber : Number ; -- number
    Dim, Aug, Super, ZDegree : Degree ; -- degree
    P1, P2, P3, ZPerson: Person ; -- person
    Inf, Ger, PPart, Pres, Impf, Perf, Fut, Pqp, SPres, SImpf, SFut, Imp, Cond : MT ; -- mood/tense

    ---
    -- classes

    -- N
    mkN : String -> String -> NF -> S ;
    mkNF : Gender -> Number -> Degree -> NF ;
    -- V
    mkV : String -> String -> VF -> S ;
    mkVF : MT -> Person -> Number -> Gender -> VF ;
    -- A
    mkA : String -> String -> AF -> S ;
    mkAF : Degree -> Gender -> Number -> AF ;

} ;
