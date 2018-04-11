abstract Morpho = {
  cat S ; NF ; Gender ; Number ; Degree ;
  fun
    mkN : String -> String -> NF -> S ;
    mkNF : Gender -> Number -> Degree -> NF ;
    Masc, Fem, Common : Gender ;
    Sg, Pl : Number ;
    Dim, Aug, Super, ZDegree : Degree ;
} ;