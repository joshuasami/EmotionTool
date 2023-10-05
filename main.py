from functions import *
from settings import *
from io_machine import *
from et_io_conversion import *
from et import *
from ec import *


# check if something was messed up in the settings-file
if list(et_labels) != ["emotion", "reduction", "intensifier", "negation", "problems", "coder"]:
    print("Hey, you changed something in the settings-file variable 'et_labels', didn't you? The keys of the dictionary have to stay the same. Please fix that.")
    exit_programm()

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

# loading intensifier-wordlist
try:
    intensifiers_raw = io.load_file(modificator_url)
    intensifiers = load_single_list(intensifiers_raw)
except:
    print("The intensifier-wordlist couldn't be loaded")
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


ec = EmotionClicker(df=df, et=et)



checker = ""
while checker not in ["0", "1"]:
    checker = input("Do you want ET to label the list or you want to 'click' it by yourself? (0 = ET, 1 = yourself)")

if checker == "0":
    automatic_labeling_decision = True

if checker == "1":
    automatic_labeling_decision = False

ec.check_df(automatic_labeling_decision)    
    
df_raw = convert_df(ec.df)

io.save_file(df_raw)

print("Thanks for using the EmotionTool")
if automatic_labeling_decision:
    print("If you want to label the table yourself now, please get the output-file out of the out folder, put it in the in folder and restart the program")