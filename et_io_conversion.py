'''This modul converts data loaded with the IOMachine into a format suitable for ET'''

from settings import *
from et_structure import *
from et_str2list import *

def load_single_list(input_structure: dict) -> list:
    '''This function converts the input dict into a list for a single word list'''
    
    out = []

    for row in input_structure.values():
        for word in row.values():
            out.append(word)

    return out

def load_double_list(input_structure: dict) -> dict:
    '''This function converts the input dict into a list for a single word list'''
    
    out = {}

    for row in input_structure.values():
        tmp_words = list(row.values())
        key = tmp_words[0]
        out[key] = tmp_words[1]

    return out

def load_df(input_structure: dict) -> list:
    '''This function converts the input file, which is to be look through with ET and EC, into the right format'''

    out = []

    for row in input_structure.values():
        answers = {}
        other_columns = {}

        for key, value in row.items():
            if key in labels:
                answers[key] = value
            else:
                other_columns[key] = value

        out.append(EmotionLine(answers, other_columns))

    return out

    