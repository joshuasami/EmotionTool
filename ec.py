from functions import *
from settings import *

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def ECMain(allText, lib):

    df = pd.read_csv(outFile, sep=";")

    df = df.fillna("")

    problems, df = checkRows(df, firstIgnore, lib, labels)


    i = 0

    solved = []

    for i in problems:

        if df['Problem'][i] == "":
            solved.append(i)
            continue

        print("\n###########\n")

        for label in labels:
            print(str(label) + ": " + str(df[label][i]))
        
        print("")

        for l in showLabels:

            print(l + ": " + str(df[l][i]))

        print("")
        if problems[i][1] == 0:
            print(allText['et']['First-Row-Problem'][language])
        elif problems[i][1] == 1:
            print(allText['et']['No-Reduction-Problem'][language])
        elif problems[i][1] == 2:
            print(allText['et']['Over-One-Problem'][language])
        elif problems[i][1] == 3:
            print(allText['et']['Nothing-Found-Problem'][language])

        print("")

        tmpProblem = []
        for x in problems[i][0]:
            tmpProblem.extend(x)

        print(allText['ec']['emotionsfound'][language])
        for x in tmpProblem:
            x.printword()

        print("")

        print("[0] - " + allText['general-phrases']['skip'][language])

        print("[1] - " + allText['ec']['own-input'][language])

        print("[2] - " + allText['ec']['99'][language])

        for index in range(3, len(tmpProblem)+ 3):
            print("[" + str(index) + "] - " + tmpProblem[index-3].emotion)

        print("")

        eingabe = ""

        while eingabe not in [str(z) for z in range(len(tmpProblem) + 3)]:
            eingabe = input(allText['general-phrases']['please-choose'][language] + ": ")

        if eingabe == "0":
            
            checker = ""

            while checker not in ["0", "1"]:
                checker = input(allText['ec']['next'][language] + " " + allText['general-phrases']['01choice'][language])

            if checker == "0":
                break

            continue

        elif eingabe == "2":

            df['Emotion'][i] = "99"
            df['Reduction'][i] = "99"
            df['Modifikator'][i] = ""
            df['Negation'][i]  = ""
            df['Problem'][i] = ""
            df['Kodierer'][i]  = coder
            solved.append(i)

        elif eingabe == "1":
            
            #### Emotion-Input

            totalChecker = True

            while totalChecker:

                tmpEingabe = input("Emotion: ")

                checker = ""

                while checker not in ["0","1"]:
                    print(allText['general-phrases']['input'][language] + ": " + tmpEingabe)
                    checker = input(allText['general-phrases']['correct'][language] + " " + allText['general-phrases']['01choice'][language])

                if checker == "1":
                    totalChecker = False

            df['Emotion'][i] = tmpEingabe


            #### Reduction-Input

            totalChecker = True

            while totalChecker:

                tmpEingabe = input("Reduction: ")

                checker = ""

                while checker not in ["0","1"]:
                    print(allText['general-phrases']['input'][language] + ": " + tmpEingabe)
                    checker = input(allText['general-phrases']['correct'][language] + " " + allText['general-phrases']['01choice'][language])

                if checker == "1":
                    totalChecker = False

            df['Reduction'][i] = tmpEingabe
            


            #### Modifier-Input

            totalChecker = True

            while totalChecker:

                tmpEingabe = input("Modifier: ")

                checker = ""

                while checker not in ["0","1"]:
                    print(allText['general-phrases']['input'][language] + ": " + tmpEingabe)
                    checker = input(allText['general-phrases']['correct'][language] + " " + allText['general-phrases']['01choice'][language])

                if checker == "1":
                    totalChecker = False

            df['Modifikator'][i] = tmpEingabe

            if tmpEingabe != "":

                #tmpSplit = tmpEingabe.split(" ")

                #tmpSplit = list(dict.fromkeys(tmpSplit))

                #for modi in tmpSplit:
                if tmpEingabe not in lib.modifiers:
                    tmpSplit = tmpEingabe.split(" ")
                    tmpSplit = list(dict.fromkeys(tmpSplit))
                    addSingleWordList(modifikatorUrl, lib.modifiers, tmpEingabe)
                    lib.modifiers.append(tmpSplit)


            #### Negation-Input

            totalChecker = True

            while totalChecker:

                tmpEingabe = input("Negation: ")

                checker = ""

                while checker not in ["0","1"]:
                    print(allText['general-phrases']['input'][language] + ": " + tmpEingabe)
                    checker = input(allText['general-phrases']['correct'][language] + " " + allText['general-phrases']['01choice'][language])

                if checker == "1":
                    totalChecker = False

            df['Negation'][i] = tmpEingabe

            if tmpEingabe != "":
                if tmpEingabe not in lib.negations:
                    tmpSplit = tmpEingabe.split(" ")
                    tmpSplit = list(dict.fromkeys(tmpSplit))
                    addSingleWordList(negationsUrl, lib.negations, tmpEingabe)
                    lib.negations.append(tmpSplit)



            if df['Emotion'][i] != "":
                if df['Modifikator'][i] in df['Emotion'][i]:
                    tmpEmo = df['Emotion'][i].replace(df['Modifikator'][i] + " ", "")
                else:
                    tmpEmo = df['Emotion'][i]

                if df['Negation'][i] in tmpEmo:
                    tmpEmo = tmpEmo.replace(" ", "").lower()
                if tmpEmo not in lib.words:
                    addWordList(lib.words, (tmpEmo, df['Reduction'][i]))
                    lib.words[tmpEmo] = df['Reduction'][i]
            
            #### Finalization

            df['Kodierer'][i]  = coder
            df['Problem'][i] = ""
            solved.append(i)


        else:
            df['Emotion'][i] = tmpProblem[int(eingabe)-3].emotion
            df['Reduction'][i] = tmpProblem[int(eingabe)-3].reduction
            df['Modifikator'][i] = tmpProblem[int(eingabe)-3].modifier
            df['Negation'][i]  = tmpProblem[int(eingabe)-3].negation
            df['Problem'][i] = ""
            df['Kodierer'][i]  = coder
            solved.append(i)


        checker = ""

        while checker not in ["0", "1"]:
            checker = input(allText['ec']['next'][language] + " " + allText['general-phrases']['01choice'][language])

        if checker == "0":
            break




    df.to_csv(outFile, sep=";", encoding='utf-8-sig', index= False)
