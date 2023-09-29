from functions import *
from settings import *
from io_machine import *
from et_io_conversion import *
from et import *
from ec import *


# creating the IOMachine instance
io = IOMachine(encoding, seperator)


# loading language file
try:
    allText = io.load_file("languages.json")
except:
    print("Could not load language file!")
    exit()

# loading wordlist
try:
    emotion_dict_raw = io.load_file(emotionwords_url)
    emotion_dict = load_double_list(emotion_dict_raw)
except:
    print("The wordlist couldn't be loaded")
    exit()

# loading negation-wordlist
try:
    negations_raw = io.load_file(negations_url)
    negations = load_single_list(negations_raw)
except:
    print("The negations-wordlist couldn't be loaded")
    exit()

# loading modificator-wordlist
try:
    intensifiers_raw = io.load_file(modificator_url)
    intensifiers = load_single_list(intensifiers_raw)
except:
    print("The modificator-wordlist couldn't be loaded")
    exit()

# creating ET
et = ET(emotion_dict = emotion_dict, intensifiers = intensifiers, negations = negations)

# loading input-file
try:
    input_file_raw = io.load_file(input_file_url)
    df = load_df(input_file_raw)
except:
    print("The input-file couldn't be loaded")





print("")

logo = """
############################################################

  _____                 _   _           _____           _ 
 | ____|_ __ ___   ___ | |_(_) ___  _ _|_   ____   ___ | |
 |  _| | '_ ` _ \ / _ \| __| |/ _ \| '_ \| |/ _ \ / _ \| |
 | |___| | | | | | (_) | |_| | (_) | | | | | (_) | (_) | |
 |_____|_| |_| |_|\___/ \__|_|\___/|_| |_|_|\___/ \___/|_|

                                    © Bräuer & Streubel  

############################################################
"""

print(logo)
print("")

checker = ""
while checker not in ["0", "1"]:
    checker = input(allText['main-menu']['welcome'][language])

if checker == "1":
    problems, df = "", ""

if checker == "0":
    problems, df = et(allText, lib)
    
    checker = ""
    print("")
    while checker not in ["0", "1"]:
        checker = input(allText['et']['continue'][language] + " " + allText['general-phrases']['01choice'][language])

if checker == "1":
    ECMain(allText, lib, problems, df)