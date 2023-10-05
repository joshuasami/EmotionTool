from re import A
from functions import *
from settings import *
from et import ET
from et_structure import EmotionLine


class EmotionClicker:
    def __init__(self, df: list, et: ET = None) -> None:
        self.df = df
        self.et = et


    def check_df(self, automatic_labeling: bool, et: ET = None, df: list = None) -> None:

        if df is None:
            df = self.df
        
        if et is None:
            et = self.et

        if automatic_labeling:
            if self.et is None:
                print("There is no instance of ET or another labelling machine loaded")
                exit_programm()
            
            for i, line in enumerate(self.df):
                self.df[i] = et.check_line(line)
        
        else:
            for i, line in enumerate(df):
                
                if line.matches == [] or line.raised_problems != []:
                    self.df[i] = self.check_line(line)
                
                if not continue_labeling:
                    break

            


    def check_line(self, line: EmotionLine) -> EmotionLine:

        self.print_line(line=line)

        eingabe = self.get_ec_decision(line)

        line = self.change_line(line=line, eingabe=eingabe)

        if len(line.emotion_word) > 0:
            
            stripped_emotion_word = line.emotion_word['emotion'].replace(line.emotion_word['intensifier'], "")
            stripped_emotion_word = stripped_emotion_word.replace(line.emotion_word['negation'], "")
            stripped_emotion_word = stripped_emotion_word.strip()

            if len(line.emotion_word['intensifier']) > 0 and line.emotion_word['intensifier'] not in self.et.intensifiers:
                self.et.intensifiers.append(line.emotion_word['intensifier'])
            
            if len(line.emotion_word['negation']) > 0 and line.emotion_word['negation'] not in self.et.negations:
                self.et.negations.append(line.emotion_word['negation'])
            
            if len(line.emotion_word['negation']) > 0 and f"nicht {stripped_emotion_word}" not in self.et.emotion_dict:
                self.et.emotion_dict[f"nicht {stripped_emotion_word}"] = line.emotion_word['reduction']

            elif len(line.emotion_word['negation']) == 0 and line.emotion_word['emotion'] not in self.et.emotion_dict:
                self.et.emotion_dict[stripped_emotion_word] = line.emotion_word['reduction']

        return line


    def print_line(self, line: EmotionLine, showLabels: list = None) -> None:

        print("\n###########\n")

        for label,value in line.answers.items():

            print(str(label) + ": " + str(value))
        
        print("")

        for l in showLabels:
            try:
                print(l + ": " + str(line.other_columns[l]))
            except:
                continue

        print("")
        
        print(f"Problems found: {', '.join([str(p) for p in line.raised_problems])}")
        
        print("")

        for col, matches in line.matches:
            print(f"Column: {col}")
            for match in matches:
                print(f"Emotion: {match['emotion']}, Reduction: {match['reduction']}, Intensifier: {match['intensifier']}, Negation: {match['negation']}")
            
            print("")
        
    def get_ec_decision(line: EmotionLine) -> str:
        print("")

        print("[1] - skip")

        print("[2] - own input")

        print("[3] - 99")

        matches_as_list = [item for sublist in line.matches.values() for item in sublist]

        for index in range(4, len(matches_as_list)+ 4):
            print("[" + str(index) + "] - " + matches_as_list[index-4]['emotion'])

        checker = ""
        checker_options = [str(x) for x in list(range(1, len(matches_as_list) + 4))]
        while checker not in checker_options:
            checker = input("Please choose: ")

        return checker

    def change_line(self, line: EmotionLine, eingabe: int) -> EmotionLine:
        


        if eingabe == "3":

            line.emotion_word['emotion'] = '99'
            line.emotion_word['reduction'] = '99'
            line.emotion_word['intensifier'] = ''
            line.emotion_word['negation'] = ''

        elif eingabe == "2":
            
            # Emotion-Input
            line.emotion_word['emotion'] = self.get_input('Emotion')
            
            # Reduction-Input
            line.emotion_word['reduction'] = self.get_input('Reduction')

            # Intensifier-Input
            line.emotion_word['intensifier'] = self.get_input('Intensifier')

            # Negation-Input
            line.emotion_word['negation'] = self.get_input('Negation')
            

        else:
            matches_as_list = [item for sublist in line.matches.values() for item in sublist]
            line.emotion_word['emotion'] = matches_as_list[eingabe-4]['emotion']
            line.emotion_word['reduction'] = matches_as_list[eingabe-4]['reduction']
            line.emotion_word['intensifier'] = matches_as_list[eingabe-4]['intensifier']
            line.emotion_word['negation'] = matches_as_list[eingabe-4]['negation']
        
        line.coder = coder

        return line

    def get_input(cat_displayed: str) -> str:

        total_checker = True

        while total_checker:

            user_input = input(cat_displayed + ": ")

            checker = ""

            while checker not in ["0","1"]:
                print("Your Input" + ": " + user_input)
                checker = input('Is this correct?' + ' ' + '(0 = No, 1 = Yes)')

            if checker == "1":
                total_checker = False


        return user_input


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