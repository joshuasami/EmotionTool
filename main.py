from functions import *
from settings import *
from et import *
from ec import *

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# load language file
try:
    allText = getJson("languages.json")
except:
    print("Could not load language file!")
    exit()

# load settings file
try:
    settings = getJson("settings.json")
except:
    print("The settings-file couldn't be open!")
    exit()

# load wordlist
try:
    mydict = getWordList()
except:
    print("The wordlist couldn't be loaded")
    exit()

# load non-words
try:
    nonwords = getSingleWordList(nonwordsUrl)
except:
    print("The nonword-wordlist couldn't be loaded")
    exit()

# load non-words
try:
    negations = getSingleWordList(negationsUrl)
except:
    print("The negations-wordlist couldn't be loaded")
    exit()

# load modificator-wordlist
try:
    modifikator = getSingleWordList(modifikatorUrl)
except:
    print("The modificator-wordlist couldn't be loaded")
    exit()


# create library
lib = library(mydict, nonwords, modifikator, negations)



print("")

logo = """
############################################################

  _____                 _   _           _____           _ 
 | ____|_ __ ___   ___ | |_(_) ___  _ _|_   ____   ___ | |
 |  _| | '_ ` _ \ / _ \| __| |/ _ \| '_ \| |/ _ \ / _ \| |
 | |___| | | | | | (_) | |_| | (_) | | | | | (_) | (_) | |
 |_____|_| |_| |_|\___/ \__|_|\___/|_| |_|_|\___/ \___/|_|

                                    © Joshua Sami Bräuer  

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