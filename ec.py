'''This is the Main Class, kind of like the controll center of the program. It is used to label the data with the help of ET'''

from functions import exit_programm
#from settings import *
from et import ET
from et_structure import EmotionLine


class EmotionClicker:
    '''This class is used to label the data with the help of ET'''

    def __init__(self, df: list, et: ET = None, coder: str = "", labels_to_show: list[str] = None, valence_pairs: dict[str] = None) -> None:
        self.df = df
        self.et = et

        if labels_to_show is None:
            labels_to_show = []
        self.labels_to_show = labels_to_show

        if valence_pairs is None:
            valence_pairs = {}
        self.valence_pairs = valence_pairs

        self.coder = coder

    def check_df(self, automatic_labeling: bool, et: ET = None, df: list = None) -> None:
        '''This function checks the whole dataframe'''

        # if no df is given, use the one from the class
        if df is None:
            df = self.df
        
        # if no et is given, use the one from the class
        if et is None:
            et = self.et

        # if automatic labeling is true, use the et to label the data
        if automatic_labeling:
            if self.et is None:
                print("There is no instance of ET or another labelling machine loaded")
                exit_programm()
            
            for i, line in enumerate(self.df):
                if self.df[i].emotion_word['emotion'] == "":
                    self.df[i] = et.check_line(line)
        
        # if automatic labeling is false, use the self.check_line function to label the data.
        # This means that the user can label the data manually
        else:
            
            # the continue_labeling variable is used to determine if the user wants to continue labeling
            continue_labeling = True
            while continue_labeling:
                for i, line in enumerate(df):

                    # the rerun variable is used to determine if the user wants to redo the labeling of a line
                    rerun = True
                    while rerun:

                        # if there is no emotion word in the line, label it    
                        if line.emotion_word['emotion'] == "":
                            tmp_line = self.check_line(line)

                            # the checker variable is used to determine if the user wants to continue labeling or redo the labeling of the line
                            checker = ""
                            while checker not in ["0", "1", "2"]:
                                checker = input("[0] Done\n[1] Next\n[2] Redo")
                            
                            if checker == "2":
                                rerun = True
                            elif checker == "0":
                                continue_labeling = False
                            
                            if checker in ["1", "0"]:
                                rerun = False

                                # if the line was labeled, we have to check if the emotion word, intensifier, or negatation are already in the et, if not, we add them
                                if len(tmp_line.emotion_word) > 0:
                                    
                                    if 'stripped_emotion' in tmp_line.emotion_word:
                                        if tmp_line.emotion_word['stripped_emotion'] not in et.emotion_dict:
                                            et.emotion_dict[tmp_line.emotion_word['stripped_emotion']] = {'reduction': tmp_line.emotion_word['reduction'], 'valenz': tmp_line.emotion_word['valenz']}

                                    for intensifier in tmp_line.emotion_word['intensifier']:
                                        if intensifier not in et.intensifiers:
                                            et.intensifiers.append(intensifier)
                                    
                                    for negation in tmp_line.emotion_word['negation']:
                                        if negation not in et.negations:
                                            et.negations.append(negation)

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

    def print_line(self, line: EmotionLine, labels_to_show: list[str] = None) -> None:
        '''This function prints the line in a readable way'''

        if labels_to_show is None:
            labels_to_show = self.labels_to_show
        
        print("\n###########\n")

        # prints all line, which possibly could contain an emotion word
        for label,value in line.answers.items():

            print(str(label) + ": " + str(value))
        
        print("")

        # prints all labels, which are in the labels_to_show list
        # if the label is not in the line, it will be skipped
        for l in labels_to_show:
            try:
                print(l + ": " + str(line.other_columns[l]))
            except KeyError:
                print(l)
                continue

        print("")
        
        # prints all problems, which were found in the line
        print(f"Problems found: {', '.join([str(p) for p in line.raised_problems])}")

        print("")

        # prints all matches, which were found in the line
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

        # creates a list of all matches
        matches_as_list = [item for sublist in line.matches.values() for item in sublist]

        # prints all matches, which were found in the line. We add 4 to the index, because the first 3 options are already taken
        for index in range(4, len(matches_as_list)+ 4):
            print("[" + str(index) + "] - " + matches_as_list[index-4]['emotion'])

        # the checker variable is used to determine if the user input is valid
        checker = ""
        checker_options = [str(x) for x in list(range(1, len(matches_as_list) + 4))]
        while checker not in checker_options:
            checker = input("Please choose: ")

        return int(checker)

    def change_line(self, line: EmotionLine, eingabe: int) -> EmotionLine:
        '''This function changes the line according to the input'''


        # if the input is 3, we set the emotion word to 99 (no emotion word found)
        if eingabe == 3:

            line.emotion_word['emotion'] = '99'
            line.emotion_word['reduction'] = '99'
            line.emotion_word['intensifier'] = []
            line.emotion_word['negation'] = []

        # if the input is 1, we return the line without changing it
        elif eingabe == 1:
            return line
        
        # if the input is 2, we ask the user for an input
        elif eingabe == 2:
            
            # Emotion-Input
            line.emotion_word['emotion'] = self.get_input('Emotion')

            # Reduction-Input
            line.emotion_word['reduction'] = self.get_input('Reduction')

            # Intensifier-Input
            line.emotion_word['intensifier'] = []
            continue_loop = True
            while continue_loop:
                intensifier_input = self.get_input('Intensifier')
                line.emotion_word['intensifier'].append(intensifier_input)
                
                if intensifier_input != "":
                    checker = ""
                    while checker not in ["0", "1"]:
                        checker = input("Do you want to add another intensifier? [0] No [1] Yes")

                        if checker not in ["0", "1"]:
                            print("Please choose 0 or 1")
                            continue
                        elif checker == "0":
                            continue_loop = False
                            break
                        elif checker == "1":
                            continue_loop = True
                            line.emotion_word['intensifier'].append(self.get_input('Intensifier'))


            # Negation-Input
            line.emotion_word['negation'] = []
            continue_loop = True
            while continue_loop:
                negation_input = self.get_input('Negation')
                line.emotion_word['negation'].append(negation_input)

                if negation_input != "":
                    checker = ""
                    while checker not in ["0", "1"]:
                        checker = input("Do you want to add another negation? [0] No [1] Yes")

                        if checker not in ["0", "1"]:
                            print("Please choose 0 or 1")
                            continue
                        elif checker == "0":
                            continue_loop = False
                            break
                        elif checker == "1":
                            continue_loop = True
                            line.emotion_word['negation'].append(self.get_input('Negation'))

            
            # Stripped-Emotion-Input
            line.emotion_word['emotion_stripped'] = self.get_input('Stripped Emotion')
            if line.emotion_word['emotion_stripped'] == "":
                line.emotion_word.pop('emotion_stripped')
            else:

                # Stripped-Reduction-Input
                line.emotion_word['reduction_stripped'] = self.get_input('Stripped Reduction')
                # Valenz-Input
                line.emotion_word['valenz'] = self.get_input('Valenz')
            
        # if the input is greater than 3, we set the emotion word to the chosen-input
        else:
            matches_as_list = [item for sublist in line.matches.values() for item in sublist]
            line.emotion_word['emotion'] = matches_as_list[eingabe-4]['emotion']
            line.emotion_word['reduction'] = matches_as_list[eingabe-4]['reduction']
            line.emotion_word['intensifier'] = matches_as_list[eingabe-4]['intensifier']
            line.emotion_word['negation'] = matches_as_list[eingabe-4]['negation']
        
        # setting the coder to the coder from the class 
        line.coder = self.coder

        return line

    def get_input(self, cat_displayed: str) -> str:
        '''This function asks the user for an input to a given category'''

        # the checker variable is used to determine if the user input is valid
        checker = ""
        continue_loop = True
        while continue_loop:
            
            user_input = input(cat_displayed + ": ")
            print("Your Input: " + user_input)
            
            while checker not in ["0", "1"]:
                checker = input("Is this correct? (0 = No, 1 = Yes)")

                if checker not in ["0", "1"]:
                    print("Please choose 0 or 1")
                    continue
                elif checker == "0":
                    user_input = input(cat_displayed + ": ")
                    print("Your Input: " + user_input)
                elif checker == "1":
                    continue_loop = False
                    break
       
       

        return user_input


