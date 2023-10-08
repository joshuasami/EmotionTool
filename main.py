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
except Exception as error:
    print("Could not load language file!")
    print(error)
    exit_programm()

# loading wordlist
try:
    emotion_dict_raw = io.load_file(emotionwords_url)
    emotion_dict = load_double_list(emotion_dict_raw)
except Exception as error:
    print("The wordlist couldn't be loaded")
    print(error)
    exit_programm()

# loading negation-wordlist
try:
    negations_raw = io.load_file(negations_url)
    negations = load_single_list(negations_raw)
except Exception as error:
    print("The negations-wordlist couldn't be loaded")
    print(error)
    exit_programm()

# loading intensifier-wordlist
try:
    intensifiers_raw = io.load_file(intensifier_url)
    intensifiers = load_single_list(intensifiers_raw)
except Exception as error:
    print("The intensifier-wordlist couldn't be loaded")
    print(error)
    exit_programm()

# creating ET
et = ET(emotion_dict = emotion_dict, intensifiers = intensifiers, negations = negations, labels_raising_problem=labels_raising_problem)

# loading input-file
try:
    header_row = io.get_csv_header(input_file_url)
    input_file_raw= io.load_file(input_file_url)
    df = load_df(input_list=input_file_raw, labels_to_look_through=labels_to_look_through, et_labels=et_labels)
except Exception as error:
    print("The input-file couldn't be loaded")
    print(error)
    exit_programm()





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
    print("You have to Options:\n[0] ET can just label the list completely for you\n[1] or go through every line, where isn't a emotion word yet and you can label it by yourself")
    checker = input("What do you want to do?")

if checker == "0":
    automatic_labeling_decision = True

if checker == "1":
    automatic_labeling_decision = False

ec.check_df(automatic_labeling_decision)    
    
df_raw = convert_df(df=df,et_labels=et_labels)

for col in et_labels.values():
    if col not in header_row:
        header_row.append(col)


io.save_file(file=outFile, output_content=df_raw, filetype="csv", header_row=header_row)

intensifiers_raw = convert_single_list(input_list=et.intensifiers, name="intensifiers")
io.save_file(file=intensifier_url, output_content=intensifiers_raw, filetype="csv")

negations_raw = convert_single_list(input_list=et.negations, name="negations")
io.save_file(file=negations_url, output_content=negations_raw, filetype="csv")

emotion_dict_raw = convert_double_list(input_dict=et.emotion_dict, row_1=et_labels['emotion'], row_2=et_labels['reduction'])
io.save_file(file=emotionwords_url, output_content=emotion_dict_raw, filetype="csv")

print("Thanks for using the EmotionTool")
if automatic_labeling_decision:
    print("If you want to label the table yourself now, please get the output-file out of the out folder, put it in the in folder and restart the program")