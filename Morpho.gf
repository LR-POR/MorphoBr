abstract Morpho = {
  cat S ; NF ; Gender ; Number ; Degree ; VF ; MT ; Mood ; Tense ; Person ;
  fun
    mkN : String -> String -> NF -> S ;
    mkNF : Gender -> Number -> Degree -> NF ;
    Masc, Fem, Common : Gender ;
    Sg, Pl, ZNumber : Number ;
    Dim, Aug, Super, ZDegree : Degree ;
    mkV : String -> String -> VF -> S ;
    mkVF : MT -> Person -> Number -> Gender -> S ;
    mkMT : Mood -> Tense -> MT ;
    Ind, Sub, Imper, Part, Ger, Inf : Mood ;
    Pres, Imperf, Fut, Past, Cond, PlusQP, ZTense: Tense ;
    P1, P2, P3, ZPerson: Person ;
} ;
{--
0	category	V:verb
1	type	M:main; A:auxiliary; S:semiauxiliary
2	mood	I:indicative; S:subjunctive; M:imperative; P:pastparticiple; G:gerund; N:infinitive
3	tense	P:present; I:imperfect; F:future; S:past; C:conditional; M:plusquamperfect
4	person	1:1; 2:2; 3:3
5	num	S:singular; P:plural
6	gen	F:feminine; M:masculine; C:common; N:neuter
--}