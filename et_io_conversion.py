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

def load_df(input_structure: dict, labels_to_look_through: list, et_labels: dict) -> list:
    '''This function converts the input file, which is to be look through with ET and EC, into the right format'''

    out = []

    for row in input_structure.values():
        answers = {}
        other_columns = {}
        et_columns = {}
        raised_problems = []

        for key, value in row.items():
            if key in labels_to_look_through:
                answers[key] = value
            elif key == et_labels['problems']:
                raised_problems.append(value)
            else:
                other_columns[key] = value

        out.append(EmotionLine(answers=answers, other_columns=other_columns, raised_problems=raised_problems))

    return out

def convert_df(df: list, et_labels: dict = None) -> dict:

    out = {}
    for i, line in enumerate(df):
        out[i] = {}
        for col, value in line.other_columns.items():
            out[i][col] = value
        for col, value in line.answers.items():
            out[i][col] = value
        

        for l in et_labels:
            out[i][l] = ""

        if line.raied_problems == [] and len(line.matches == 1):
            for col, value in line.matches[1]:
                out[i][et_labels[col]] = value


        out[i][et_labels['problem']] = line.raied_problems

        
