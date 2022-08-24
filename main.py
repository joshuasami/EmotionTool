from functions import *
from settings import *
from et import *
from ec import *

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


mydict = getWordList()
nonwords = getSingleWordList(nonwordsUrl)
negations = getSingleWordList(negationsUrl)
modifikator = getSingleWordList(modifikatorUrl)

lib = library(mydict, nonwords, modifikator, negations)

allText = getText()

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