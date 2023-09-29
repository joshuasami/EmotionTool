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
et = ET(emotion_dict = emotion_dict, intensifiers = intensifiers, negations = negations)

test_line1 = "ich bin nicht sehr sehr glücklich, aber dann doch eher etwas nicht keine lust"
test_line1 = str2list(test_line1)
test_answer1 = [[('keine', 'Lust'), [], [['nicht']]], [('glücklich',), [['sehr'], ['sehr']], [['nicht']]]]

test_line2 = "mir geht es sehr gut"
test_line2 = str2list(test_line2)
test_answer2 = [[('gut',), [['sehr']], []]]

test_line3 =  "fröhlich"
test_line3 = str2list(test_line3)
test_answer3 = [[("fröhlich",),[],[]]]

test_line4 = ""
test_line4 = str2list(test_line4)
test_answer4 = [[[],[],[]]]

def test_multiple_assert_statements():
    assert et.check_line(test_line1) == test_answer1
    assert et.check_line(test_line2) == test_answer2
    assert et.check_line(test_line3) == test_answer3
    assert et.check_line(test_line4) == test_answer4

