import json

morphobr_to_bosque = {
    'A': ['Cat=ADJ'],
    'ADV': ['Cat=ADV'],
    'N': ['Cat=NOUN'],
    'V': ['Cat=VERB'],
    'F': ['Gender=Fem'],
    'M': ['Gender=Masc'],
    'SG': ['Number=Sing'],
    'PL': ['Number=Plur'],
    'NEG': ['Polarity=Neg'],
    'SUPER': ['Degree=Abs'],
    'DIM': ['Degree=Dim'],
    'AUG': ['Degree=Aug'],
    '1': ['Person=1'],
    '2': ['Person=2'],
    '3': ['Person=3'],
    'INF': ['VerbForm=Inf'],
    'GRD': ['VerbForm=Ger'],
    'PTPST': ['VerbForm=Part','Tense=Past'],
    'PRS': ['Mood=Ind','Tense=Pres'],
    'IMPF': ['Mood=Ind','Tense=Imp'],
    'PRF': ['Mood=Ind','Tense=Past'],
    'FUT': ['Mood=Ind','Tense=Fut'],
    'PQP': ['Mood=Ind','Tense=Pqp'],
    'SBJR': ['Mood=Sub','Tense=Pres'],
    'SBJP': ['Mood=Sub','Tense=Imp'],
    'SBJF': ['Mood=Sub','Tense=Fut'],
    'IMP': ['Mood=Imp'],
    'COND': ['Mood=Cod']     
}

with open('morphobr_to_bosque.json', 'w') as f:
    json.dump(morphobr_to_bosque, f)
