abstract Morpho = {
  cat S ; -- entry
      Form ; Lemma ;
      NF ; VF ; AF ; AdvF ; -- class features
      -- features
      Gender ; Number ; Degree ; Person ;
      VT ; -- Mood + Tense
      AdvT ; -- general or negative
  fun
    ---
    -- features
    Masc, Fem, Common, ZGender : Gender ; -- gender
    Sg, Pl, InvN, ZNumber : Number ; -- number
    Dim, Aug, Super, ZDegree : Degree ; -- degree
    P1, P2, P3, ZPerson: Person ; -- person
    Inf, Ger, PPart, Pres, Impf, Perf, Fut, Pqp, SPres, SImpf, SFut, Imp, Cond : VT ; -- V type
    GAdv, NAdv : AdvT ;

    mkForm : String -> Form ;
    mkLemma : String -> Lemma ;

    ---
    -- classes

    -- N
    mkN : Form -> Lemma -> NF -> S ;
    mkNF : Gender -> Number -> Degree -> NF ;
    -- V
    mkV : Form -> Lemma -> VF -> S ;
    mkVF : VT -> Person -> Number -> Gender -> VF ;
    -- A
    mkA : Form -> Lemma -> AF -> S ;
    mkAF : Degree -> Gender -> Number -> AF ;
    -- Adv
    mkAdv : Form -> Lemma -> AdvF -> S ;
    mkAdvF : AdvT -> AdvF ;

} ;
