'''This file contains all settings for the program.'''
# Please look through all possible settings once. Their might be somithing for you to change for the programm to work correctly.
# IMPORT: Don't save the words, which are written in capital-letters. These are variable-names and changing them will result in an error and break the program!

# Filepath of the input-file
INPUT_FILE_URL = "test-" +  "in/et_in_file.csv"

# Filepath of the Emotion-Dictinary
# IMPORTANT: Please name the columns of the dictionary 'emotion', 'reduction', and 'valence'!
EMOTION_WORDS_URL = "test-" +  "lists/words_valence.csv"

# If a word has a valence on the key side of the dictionary (the word before the :), the word on the other side is used as a reduction, if there is one negation before the emotion term.
VALENCE_PAIRS = {
    "positiv":"negativ",
    "negativ":"positiv",
    "neutral":"neutral"
    }

# Filepath of the negation-wordlist
NEGATIONS_URL = "test-" +  "lists/negation.csv"

# Filepath of the intensifier-wordlist
INTENSIFIER_URL = "test-" +  "lists/modifikator.csv"

# Filepath of the output-file
# IMPORTANT: MUST BE A CSV-FILE
OUTPUT_FILE_URL = "test-" +  "out/ETout_KEeKS_LS_EFB_09062023_605-647.csv"

# Columns which are to be searched for emotions by ET
LABELS_TO_LOOK_THROUGH = [
    'Verständnisfrage',
    'Frage 1', 
    'Nachfrage 1', 
    'Nachfrage 2', 
    'Nachfrage 3', 
    'Nachfrage 4'
    ]

# Columns which raise an error, if a match is found in them
LABELS_RAISING_PROBLEMS = ['Verständnisfrage']

# column-names, which should be shown next to the default columns, when "clicking through the lines".
LABELS_TO_SHOW = ["ID subject", "vignette"]

# Name of the coder, which is noted in the output-file
CODER = "JSB"

# Column-names for the ET specific columns. 
# This is a dictionary format (key:value). The key (e.g. "emotion") is the name of the column inside the program. The value (e.g. "Emotion") is the name of the column in your input.file.
# IMPORTANT!!!: Don't change the keys (e.g. "emotion")! Only change the values (e.g. "Emotion")! Changing the keys will result in an error and break the program!
ET_LABELS = {
    "emotion":"Emotion", 
    "reduction":"Reduction", 
    "intensifier":"Intensifier", 
    "negation":"Negation", 
    "problems": "Problems", 
    "coder": "Coder"
    }

WORDLIST_LABELS = {
    "emotion": "emotion",
    "reduction": "reduction",
    "valence": "valence",
    "intensifier": "intensifier",
    "negation": "negation"
}

NO_EMOTION_FOUND_LABEL = "99"

# Encoding of al the input-files
ENCODING = "utf-8-sig"

# Seperator for the csv-files
SEPERATOR = ";"

# Seperator inside of string 
STRING_SEPERATOR = ","


LOGO = """
    ############################################################

    _____                 _   _           _____           _ 
    | ____|_ __ ___   ___ | |_(_) ___  _ _|_   ____   ___ | |
    |  _| | '_ ` _ \ / _ \| __| |/ _ \| '_ \| |/ _ \ / _ \| |
    | |___| | | | | | (_) | |_| | (_) | | | | | (_) | (_) | |
    |_____|_| |_| |_|\___/ \__|_|\___/|_| |_|_|\___/ \___/|_|

                                        © Bräuer & Streubel  

    ############################################################
    """