'''This modul converts data loaded with the IOMachine into a format suitable for ET'''

from et_structure import *


def load_single_list(input_list: list[dict]) -> list:
    '''This function converts the input dict into a list for a single word list'''
    
    out = []
    for row in input_list:
        for word in row.values():
            out.append(word)

    return out

def load_double_list(input_list: list[dict]) -> dict:
    '''This function converts the input dict into a list for a single word list'''
    
    out = {}

    for row in input_list:
        vals = list(row.values())
        out[vals[0]] = vals[1]

    return out

def load_df(input_list: list[dict], labels_to_look_through: list, et_labels: dict) -> list[EmotionLine]:
    '''This function converts the input file, which is to be look through with ET and EC, into the right format'''

    out = []

    for row in input_list:
        answers = {}
        other_columns = {}
        emotion_word = {'emotion':'', 'reduction':'', 'intensifier':'', 'negation':''}
        raised_problems = []
        coder = ""

        for key, value in row.items():
            if key in labels_to_look_through:
                answers[key] = value
            elif key == et_labels['problems']:
                raised_problems = [int(i) for i in value.split()]
            elif key == et_labels['coder']:
                coder = value
            elif key == et_labels['emotion']:
                emotion_word['emotion'] = value
            elif key == et_labels['reduction']:
                emotion_word['reduction'] = value
            elif key == et_labels['intensifier']:
                emotion_word['intensifier'] = value
            elif key == et_labels['negation']:
                emotion_word['negation'] = value
            else:
                other_columns[key] = value

        out.append(EmotionLine(answers=answers, other_columns=other_columns, emotion_word=emotion_word, coder=coder,raised_problems=raised_problems))

    return out

def convert_single_list(input_list: list, name: str) -> list[dict]:

    out = []

    for line in input_list:
        tmp_out = {}
        tmp_out[name] = line
        out.append(tmp_out)

    return out

def convert_double_list(input_dict: dict, row_1: str, row_2: str) -> list[dict]:

    out = []

    for key,value in input_dict.items():
        tmp_out = {}
        tmp_out[row_1] = key
        tmp_out[row_2] = value
        out.append(tmp_out)

    return out

def convert_df(df: list[EmotionLine], et_labels: dict = None) -> list[dict]:

    out = []
    
    for line in df:
        tmp_out = {}

        tmp_out.update(line.answers)
        tmp_out.update(line.other_columns)
        tmp_out.update({et_labels['emotion']:line.emotion_word['emotion']})
        tmp_out.update({et_labels['reduction']:line.emotion_word['reduction']})
        tmp_out.update({et_labels['intensifier']:line.emotion_word['intensifier']})
        tmp_out.update({et_labels['negation']:line.emotion_word['negation']})
        tmp_out.update({et_labels['problems']:" ".join([str(p) for p in line.raised_problems])})
        tmp_out.update({et_labels['coder']:line.coder})

        out.append(tmp_out)
    
    return out