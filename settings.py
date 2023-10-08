'''This file contains all settings for the program.'''
# Please look through all possible settings once. Their might be somithing for you to change for the programm to work correctly.
# IMPORT: Don't save the words, which are written in capital-letters. These are variable-names and changing them will result in an error and break the program!

# Filepath of the input-file
INPUT_FILE_URL = "in/et_in_file.csv"

# Filepath of the Emotion-Dictinary
EMOTION_WORDS_URL = "lists/words.csv"

# Filepath of the negation-wordlist
NEGATIONS_URL = "lists/negation.csv"

# Filepath of the intensifier-wordlist
INTENSIFIER_URL = "lists/modifikator.csv"

# Filepath of the output-file
OUTPUT_FILE = "out/ETout_KEeKS_LS_EFB_09062023_605-647.csv"

# Columns which are to be searched for emotions by ET
LABELS_TO_LOOK_THROUGH = ['Verständnisfrage',
                          'Frage 1', 
                          'Nachfrage 1', 
                          'Nachfrage 2', 
                          'Nachfrage 3', 
                          'Nachfrage 4']

# Columns which raise an error, if a match is found in them
LABELS_RAISING_PROBLEMS = ['Verständnisfrage']

# column-names, which should be shown next to the default columns, when "clicking through the lines".
LABELS_TO_SHOW = ["vignette"]

# Name of the coder, which is noted in the output-file
CODER = "JSB"

# Column-names for the ET specific columns. 
# This is a dictionary format (key:value). The key (e.g. "emotion") is the name of the column inside the program. The value (e.g. "Emotion") is the name of the column in your input.file.
# IMPORTANT!!!: Don't change the keys (e.g. "emotion")! Only change the values (e.g. "Emotion")! Changing the keys will result in an error and break the program!
ET_LABELS = {"emotion":"Emotion", 
             "reduction":"Reduction", 
             "intensifier":"Intensifier", 
             "negation":"Negation", 
             "problems": "Problems", 
             "coder": "Coder"}

# Encoding of al the input-files
ENCODING = "utf8"

# Seperator for the csv-files
SEPERATOR = ";"
