from re import A
from functions import *
from settings import *
from et import ET
from et_structure import EmotionLine


class EmotionClicker:
    '''This class is used to label the data with the help of ET'''

    def __init__(self, df: list, et: ET = None) -> None:
        self.df = df
        self.et = et


    def check_df(self, automatic_labeling: bool, et: ET = None, df: list = None) -> None:
        '''This function checks the whole dataframe'''

        # if no df is given, use the one from the class
        if df is None:
            df = self.df
        
        # if no et is given, use the one from the class
        if et is None:
            et = self.et

        
        if automatic_labeling:
            if self.et is None:
                print("There is no instance of ET or another labelling machine loaded")
                exit_programm()
            
            for i, line in enumerate(self.df):
                self.df[i] = et.check_line(line)
        
        else:
            continue_labeling = True
            while continue_labeling:
                for i, line in enumerate(df):
                    rerun = True
                    while rerun:    
                        if line.emotion_word['emotion'] == "":
                            tmp_line = self.check_line(line)

                            checker = ""
                            while checker not in ["0", "1", "2"]:
                                checker = input("[0] Done\n[1] Next\n[2] Redo")

                            if checker == "2":
                                rerun = True
                            elif checker == "0":
                                continue_labeling = False
                            
                            if checker in ["1", "0"]:
                                rerun = False

                                if len(tmp_line.emotion_word) > 0:
                                    
                                    stripped_emotion_word = tmp_line.emotion_word['emotion'].replace(tmp_line.emotion_word['intensifier'], "")
                                    stripped_emotion_word = stripped_emotion_word.replace(tmp_line.emotion_word['negation'], "")
                                    stripped_emotion_word = stripped_emotion_word.strip()

                                    if len(tmp_line.emotion_word['intensifier']) > 0 and tmp_line.emotion_word['intensifier'] not in self.et.intensifiers:
                                        self.et.intensifiers.append(tmp_line.emotion_word['intensifier'])
                                    
                                    if len(tmp_line.emotion_word['negation']) > 0 and tmp_line.emotion_word['negation'] not in self.et.negations:
                                        self.et.negations.append(tmp_line.emotion_word['negation'])
                                    
                                    if len(tmp_line.emotion_word['negation']) > 0 and f"nicht {stripped_emotion_word}" not in self.et.emotion_dict:
                                        self.et.emotion_dict[f"nicht {stripped_emotion_word}"] = tmp_line.emotion_word['reduction']

                                    elif len(tmp_line.emotion_word['negation']) == 0 and tmp_line.emotion_word['emotion'] not in self.et.emotion_dict:
                                        self.et.emotion_dict[stripped_emotion_word] = tmp_line.emotion_word['reduction']

                                self.df[i] = tmp_line

                        else:
                            rerun = False
                        
                    if not continue_labeling:
                        break

            


    def check_line(self, line: EmotionLine) -> EmotionLine:
        '''This function checks a single line'''

        line = self.et.check_line(line=line)
        
        self.print_line(line=line)

        eingabe = self.get_ec_decision(line)

        line = self.change_line(line=line, eingabe=eingabe)

        return line


    def print_line(self, line: EmotionLine, showLabels: list = None) -> None:
        '''This function prints the line in a readable way'''

        if showLabels is None:
            showLabels = []
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

        for col, matches in line.matches.items():
            print(f"Column: {col}")
            for match in matches:
                print(f"Emotion: {match['emotion']}, Reduction: {match['reduction']}, Intensifier: {match['intensifier']}, Negation: {match['negation']}")
            
            print("")
        
    def get_ec_decision(self, line: EmotionLine) -> str:
        '''This function asks the user for the decision'''
        
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

        return int(checker)

    def change_line(self, line: EmotionLine, eingabe: int) -> EmotionLine:
        '''This function changes the line according to the input'''


        if eingabe == 3:

            line.emotion_word['emotion'] = '99'
            line.emotion_word['reduction'] = '99'
            line.emotion_word['intensifier'] = ''
            line.emotion_word['negation'] = ''

        elif eingabe == 1:
            return line
        
        elif eingabe == 2:
            
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

    def get_input(self, cat_displayed: str) -> str:
        '''This function asks the user for an input to a given category'''

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

