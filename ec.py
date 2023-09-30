from re import A
from functions import *
from settings import *
from et import ET
from et_structure import EmotionLine


class EmotionClicker:
    def __init__(self, df: list, et: ET = None) -> None:
        self.df = df
        self.et = et


    def check_df(self, df: list = None) -> list:

        if df is None:
            df = self.df

        # 0 = Verständnisfrage
        # 1 = no Reduction
        # 2 = over 2
        # 3 = 0
        problems = {}
        check = []
        for i,line in enumerate(df):

            if line.matches is not None:
                continue

            
            # checking all col
            out = []
            for key, col in line.anwers.items():
                out.append({key:self.et.check_line(col)})
            
            
            counter = 0
            for y in out:
                counter += len(y)

            if counter == 1:            
                if self.first_ignore:
                    if out[0] != []:
                        problems[i] = [out, 0]
                        continue
                
                for i in out:
                    if i != []:
                        df['Emotion'][ind] = i[0].emotion
                        df['Reduction'][ind] = i[0].reduction
                        df['Modifikator'][ind] = i[0].modifier
                        df['Negation'][ind]  = i[0].negation
                        df['Kodierer'][ind]  = "E.T."
                        df['Problem'][ind]  = ""
                if df['Reduction'][ind] == "":
                    problems[ind] = [out, 1]
            
            elif counter > 1:
                emos = []
                for z in range(len(out)):
                    for i in out[z]:
                        if i != []:
                            emos.append(i.emotion)
                            #for y in out:
                            #    if y != []:
                            #        if i.emotion != y.emotion:
                            #            sameEmo = False
                            
                if len(Counter(emos).values()) == 1:
                    for i in out:
                        if i != []:
                            df['Emotion'][ind] = i[0].emotion
                            df['Reduction'][ind] = i[0].reduction
                            df['Modifikator'][ind] = i[0].modifier
                            df['Negation'][ind]  = i[0].negation
                            df['Kodierer'][ind]  = "E.T."
                            df['Problem'][ind]  = ""
                else:
                    problems[ind] = [out, 2]
            else:
                problems[ind] = [out, 3]

            check.append(counter)

        for ind in problems:
            df['Problem'][ind] = problems[ind][1]

        

        return problems, df

    def check_line(self, line: str) -> list:
        if self.et is not None:
            for 



def ECMain(allText, lib, problems, df):

    if problems == "" or isinstance(df, str):

        df = pd.read_csv(outFile, sep=seperator, encoding='utf-8-sig')

        df = df.fillna("")

        problems, df = checkRows(df, firstIgnore, lib, labels)


    ECRun(allText, lib, df, problems)

def ECRun(allText, lib, df, problems):
    i = 0

    rerun = False

    solved = []

    for i in problems:

        if df['Problem'][i] == "":
            solved.append(i)
            continue

        eingabe, tmpProblem = ECPrint(allText,i, problems, df)



        if eingabe == "1":
            
            checker = checker01(allText)

            if checker == "0":
                break

            continue

        elif eingabe == "3":

            df['Emotion'][i] = "99"
            df['Reduction'][i] = "99"
            df['Modifikator'][i] = ""
            df['Negation'][i]  = ""
            df['Kodierer'][i]  = coder
            solved.append(i)

        elif eingabe == "2":
            
            #### Emotion-Input

            tmpEingabe, df = getInput(allText, df, i, 'Emotion')

            #### Reduction-Input

            tmpEingabe, df = getInput(allText, df, i, 'Reduction')
            
            #### Modifier-Input

            tmpEingabe, df = getInput(allText, df, i, 'Modifikator')

            if tmpEingabe != "":
                if tmpEingabe not in lib.modifiers:
                    tmpSplit = tmpEingabe.split(" ")
                    tmpSplit = list(dict.fromkeys(tmpSplit))
                    addSingleWordList(modifikatorUrl, lib.modifiers, tmpEingabe)
                    lib.modifiers.append(tmpSplit)

            #### Negation-Input

            tmpEingabe, df = getInput(allText, df, i, 'Negation')

            if tmpEingabe != "":
                if tmpEingabe not in lib.negations:
                    tmpSplit = tmpEingabe.split(" ")
                    tmpSplit = list(dict.fromkeys(tmpSplit))
                    addSingleWordList(negationsUrl, lib.negations, tmpEingabe)
                    lib.negations.append(tmpSplit)



            if df['Emotion'][i] != "":
                if (df['Modifikator'][i] in df['Emotion'][i]) and (df['Modifikator'][i] != ""):
                    tmpEmo = df['Emotion'][i].replace(df['Modifikator'][i] + " ", "")
                else:
                    tmpEmo = df['Emotion'][i]

                if (df['Negation'][i] in tmpEmo) and (df['Negation'][i] != ""):
                    tmpEmo = tmpEmo.replace(df['Negation'][i], "nicht").lower()
                if tmpEmo not in lib.words:
                    addWordList(lib.words, (tmpEmo, df['Reduction'][i]))
                    lib.words[tmpEmo] = df['Reduction'][i]
            
            #### Finalization

            df['Kodierer'][i]  = coder
            solved.append(i)


        else:
            df['Emotion'][i] = tmpProblem[int(eingabe)-4].emotion
            df['Reduction'][i] = tmpProblem[int(eingabe)-4].reduction
            df['Modifikator'][i] = tmpProblem[int(eingabe)-4].modifier
            df['Negation'][i]  = tmpProblem[int(eingabe)-4].negation
            df['Kodierer'][i]  = coder
            solved.append(i)


        checker = ""

        while checker not in ["0", "1", "2"]:
            checker = input("\n" + allText['ec']['nextorback'][language])
        
        if eingabe == "2":
            rerun = True

        if checker == "0":
            rerun = False
            break

        if checker == "2":
            solved.pop()

            for solve in solved:
                try:
                    problems.pop(solve)
                except KeyError:
                    pass
        
            ECRun(allText, lib, df, problems)
            return 0
            
    
        if rerun:
            for solve in solved:
                try:
                    problems.pop(solve)
                except KeyError:
                    pass
            problems, df = checkRows(df, firstIgnore, lib, labels)
            ECRun(allText, lib, df, problems)
            return 0

    df['Problem'] = pd.to_numeric(df['Problem'], downcast='integer')
    df.to_csv(outFile, sep=seperator, encoding='utf-8-sig', index= False)

def ECPrint(allText, i, problems, df):

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

    print("[1] - " + allText['general-phrases']['skip'][language])

    print("[2] - " + allText['ec']['own-input'][language])

    print("[3] - " + allText['ec']['99'][language])

    for index in range(4, len(tmpProblem)+ 4):
        print("[" + str(index) + "] - " + tmpProblem[index-4].emotion)

    print("")

    eingabe = ""

    while eingabe not in [str(z) for z in range(1, len(tmpProblem) + 4)]:
        eingabe = input(allText['general-phrases']['please-choose'][language] + ": ")

    return eingabe, tmpProblem

def getInput(allText, df, i, cat):

    totalChecker = True

    while totalChecker:

        tmpEingabe = input(cat + ": ")

        checker = ""

        while checker not in ["0","1"]:
            print(allText['general-phrases']['input'][language] + ": " + tmpEingabe)
            checker = input(allText['general-phrases']['correct'][language] + " " + allText['general-phrases']['01choice'][language])

        if checker == "1":
            totalChecker = False

    df[cat][i] = tmpEingabe

    return tmpEingabe, df