from settings import *
from io_machine import *
from et_io_conversion import *
from et import *

import pytest


# creating the IOMachine instance
io = IOMachine(encoding, seperator)


# loading language file
try:
    allText = io.load_file("languages.json")
except:
    print("Could not load language file!")
    quit()

# loading wordlist
try:
    emotion_dict_raw = io.load_file(emotionwords_url)
    emotion_dict = load_double_list(emotion_dict_raw)
except:
    print("The wordlist couldn't be loaded")
    quit()

# loading negation-wordlist
try:
    negations_raw = io.load_file(negations_url)
    negations = load_single_list(negations_raw)
except:
    print("The negations-wordlist couldn't be loaded")
    quit()

# loading modificator-wordlist
try:
    intensifiers_raw = io.load_file(modificator_url)
    intensifiers = load_single_list(intensifiers_raw)
except:
    print("The modificator-wordlist couldn't be loaded")
    quit()

# creating ET
et = ET(emotion_dict = emotion_dict, intensifiers = intensifiers, negations = negations, labels_raising_problem=labels_raising_problem)

test_line1 = "ich bin nicht sehr sehr glücklich, aber dann doch eher etwas nicht keine lust"
#test_answer1 = [[('keine', 'Lust'), ['lustlos'], [], [['nicht']]], [('glücklich',), ['glücklich'], [['sehr'], ['sehr']], [['nicht']]]]
test_answer1 = [['keine Lust', 'lustlos', [], ['nicht']], ['glücklich', 'glücklich', ['sehr', 'sehr'], ['nicht']]]

test_line2 = "mir geht es sehr gut"
test_answer2 = [['gut', 'positiv', ['sehr'], []]]

test_line3 =  "fröhlich"
test_answer3 = [["fröhlich", 'fröhlich', [],[]]]

test_line4 = ""
test_answer4 = [["","",[],[]]]

def test_multiple_assert_statements():
    assert et.check_for_emotion(test_line1) == test_answer1
    assert et.check_for_emotion(test_line2) == test_answer2
    assert et.check_for_emotion(test_line3) == test_answer3
    assert et.check_for_emotion(test_line4) == test_answer4


tmp = load_df(io.load_file("in/et_in_file.csv"), labels_to_look_through)
i = 0
for i in range(1):
    tmp_line = et.check_line(tmp[i])
    print(tmp_line.answers)
    print(tmp_line.other_columns)
    print(tmp_line.matches)
    print(tmp_line.raised_problems)




