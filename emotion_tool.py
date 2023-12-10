'''This is the Main Class, kind of like the controll center of the program. It is used to label the data with the help of ET'''

from et import ET
from et_structure import EmotionLine, DataFrame, EmotionWord
from user_interface import UserInterface
import copy


class EmotionTool:
    '''This class is used to label the data with the help of ET'''

    def __init__(self, ui: UserInterface, df: DataFrame, et: ET = None, coder: str = "", labels_to_show: list[str] = None, valence_pairs: dict[str] = None, no_emotion_found_label: str = "99") -> None:
        
        self.ui = ui
        self.df = df
        self.et = et
        self.no_emotion_found_label = no_emotion_found_label

        if labels_to_show is None:
            labels_to_show = []
        self.labels_to_show = labels_to_show

        if valence_pairs is None:
            valence_pairs = {}
        self.valence_pairs = valence_pairs

        self.coder = coder

        self.problem_dict = {
            "0":"Match in a marked column",
            "1":"No reduction found",
            "2":"More than one Emotion found",
            "3":"No Emotions were found",
            "4":"More than one Negation found" 
            }

    def check_df(self) -> None:
        '''This function checks the whole dataframe'''
        
        if self.et is None:
            self.ui.display_message("There is no instance of ET or another labelling machine loaded")
            return None
        
        # the dataframe is labeled by ET automaticly once
        self.automatic_labeling()
        self.df.save_df()

        # printing the problems, which were found in the dataframe
        problem_count = self.df.get_problems_count()
        self.ui.display_message(f"{problem_count.pop('total')} problems were found in {problem_count.pop('lines_with_problems')} lines in the dataframe")
        for problems, count in problem_count.items():
            self.ui.display_message(f"{self.problem_dict[problems]}: {count}")
        
        self.ui.print_empty_line()

        # asking the user, if they want to label the list whole list at once or line by line
        checker = ""
        decision_map = {"0": True, "1": False}
        while checker not in decision_map:
            self.ui.display_message("You have to Options:\n[0] ET can label the list completely for you\n[1] or you go through every line, where isn't a emotion word yet and you can label it by yourself. ET is still helping you with labeling")
            checker = self.ui.get_input("What do you want to do?")

        automatic_labeling_decision = decision_map.get(checker, False)
        
        # if automatic labeling is false, use the self.check_line function to label the data.
        # This means that the user can label the data manually
        if automatic_labeling_decision:
            return None
        
        # the continue_labeling variable is used to determine if the user wants to continue labeling
        continue_labeling = True

        while continue_labeling:

            for line in self.df.iterate_rows():

                # the rerun variable is used to determine if the user wants to redo the labeling of a line
                rerun = True
                while rerun:
                    # if the line is already labeled, we skip it  
                    if line.is_labelled:
                        break

                    # the line is labeled
                    tmp_line = copy.deepcopy(line)
                    tmp_line = self.check_line(tmp_line)

                    # the checker variable is used to determine if the user wants to continue labeling or redo the labeling of the line
                    checker = ""
                    decision_map = {"0": "Done", "1": "Next", "2": "Redo"}

                    while checker not in ["0", "1", "2"]:
                        checker = self.ui.get_input("[0] Done\n[1] Next\n[2] Redo")
                    
                    
                    decision = decision_map.get(checker, "Done")

                    if decision == "Redo":
                        continue

                    if decision in ["Done", "Next"]:
                        rerun = False

                    if decision == "Done":
                        continue_labeling = False
                    
                    line.update_from_other(tmp_line)
                    new_word_added = self.add_words(line=line)

                    if line.is_labelled:
                        self.df.save_df()


                    if new_word_added and self.et is not None:
                        self.et.wordlist.save_wordlists()
                        self.automatic_labeling()

                if not continue_labeling:
                    break

    def add_words(self, line: EmotionLine) -> bool:
        '''This function adds the words from the line to et'''
        
        new_words_added = False

        # if the line was labeled, we have to check if the emotion word, modifier, or negatation are already in the et, if not, we add them
        if line.emotion_word != {}:
            if line.emotion_word.exists_stripped():
                if not self.et.wordlist.is_emotion(line.emotion_word.get_stripped_emotion()):
                    self.et.wordlist.add_emotion(emotion=line.emotion_word.get_stripped_emotion(), 
                                                 reduction=line.emotion_word.get_stripped_reduction(), 
                                                 valence=line.emotion_word.get_valence())
                    new_words_added = True

            for modifier in line.emotion_word.get_modifier():
                if not self.et.wordlist.is_modifier(modifier):
                    self.et.wordlist.add_modifier(modifier)
                    new_words_added = True
            
            for negation in line.emotion_word.get_negation():
                if not self.et.wordlist.is_negation(negation):
                    self.et.wordlist.add_negation(negation)
                    new_words_added = True

        return new_words_added
          
    def automatic_labeling(self) -> None:
        '''This function labels the data automatically'''
        for line in self.df.iterate_rows():
            if not line.is_labelled:
                line = self.et.check_line(line)

    def check_line(self, line: EmotionLine) -> EmotionLine:
        '''This function checks a single line'''

        line = self.et.check_line(line=line)
        
        self.print_line(line=line)

        eingabe = self.get_ec_decision(line)

        line = self.change_line(line=line,eingabe=eingabe)

        return line

    def print_line(self, line: EmotionLine, labels_to_show: list[str] = None) -> None:
        '''This function prints the line in a readable way'''

        if labels_to_show is None:
            labels_to_show = self.labels_to_show
        self.ui.print_empty_line()
        self.ui.display_message("####################")
        self.ui.print_empty_line()
        # prints all line, which possibly could contain an emotion word
        for label,value in line.answers.items():

            self.ui.display_message(str(label) + ": " + str(value))
        
        self.ui.print_empty_line()

        # prints all labels, which are in the labels_to_show list
        # if the label is not in the line, it will be skipped
        for l in labels_to_show:
            try:
                self.ui.display_message(l + ": " + str(line.other_columns[l]))
            except KeyError:
                self.ui.display_message(l)
                continue

        self.ui.print_empty_line()
        
        # prints all problems, which were found in the line
        # explanation of raised problem-codes
        # 0 = match in marked column
        # 1 = no reduction
        # 2 = over 1
        # 3 = 0 matches
        # 4 = more than one negations found
        
        self.ui.display_message(f"Problems found: {', '.join([self.problem_dict[p] for p in line.raised_problems])}")

        self.ui.print_empty_line()

        # prints all matches, which were found in the line
        for col, matches in line.matches.items():
            self.ui.display_message(f"Column: {col}")
            for match in matches:
                self.ui.display_message(match)

            self.ui.print_empty_line()
        
    def get_ec_decision(self, line: EmotionLine) -> str:
        '''This function asks the user for the decision'''
        
        self.ui.display_message("")

        self.ui.display_message("[1] - skip")

        self.ui.display_message("[2] - own input")

        self.ui.display_message(f"[3] - {self.no_emotion_found_label}")

        # creates a list of all matches
        matches_as_list = [item for sublist in line.matches.values() for item in sublist]

        # removes duplicates from the list
        matches_as_list = list(dict.fromkeys(matches_as_list))

        # prints all matches, which were found in the line. We add 4 to the index, because the first 3 options are already taken
        for index in range(4, len(matches_as_list)+ 4):
            self.ui.display_message("[" + str(index) + "] - " + matches_as_list[index-4].get_emotion())

        # the checker variable is used to determine if the user input is valid
        checker = ""
        checker_options = [str(x) for x in list(range(1, len(matches_as_list) + 4))]
        while checker not in checker_options:
            checker = self.ui.get_input("Please choose: ")

        return int(checker)

    def change_line(self, line: EmotionLine, eingabe: int) -> EmotionLine:
        '''This function changes the line according to the input'''


        # if the input is 3, we set the emotion word to 99 (no emotion word found)
        if eingabe == 3:

            line.emotion_word = EmotionWord(emotion=self.no_emotion_found_label, reduction=self.no_emotion_found_label, modifier=[], negation=[])

        # if the input is 1, we return the line without changing it
        elif eingabe == 1:
            return line
        
        # if the input is 2, we ask the user for an input
        elif eingabe == 2:
            
            # Emotion-Input
            input_emotion = self.get_input('Emotion')

            # Reduction-Input
            input_reduction = self.get_input('Reduction')

            # Modifier-Input
            input_modifiers = []
            continue_loop = True
            while continue_loop:
                modifier_input = self.get_input('Modifier')
                input_modifiers.append(modifier_input)
                
                if modifier_input != "":
                    checker = ""
                    while checker not in ["0", "1"]:
                        checker = input("Do you want to add another modifier? [0] No [1] Yes")

                        if checker not in ["0", "1"]:
                            print("Please choose 0 or 1")
                            continue
                        elif checker == "0":
                            continue_loop = False
                            break
                        elif checker == "1":
                            continue_loop = True
                            checker = ""
                            input_modifiers.append(self.get_input('Modifier'))
                else:
                    continue_loop = False


            # Negation-Input
            input_negations = []
            continue_loop = True
            while continue_loop:
                negation_input = self.get_input('Negation')
                input_negations.append(negation_input)

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
                            checker = ""
                            input_negations.append(self.get_input('Negation'))
                else:
                    continue_loop = False

            line.emotion_word = EmotionWord(emotion=input_emotion, 
                                            reduction=input_reduction, 
                                            modifier=input_modifiers, 
                                            negation=input_negations)
            
            # Stripped-Emotion-Input
            input_stripped_emotion = self.get_input('Stripped Emotion')
            if input_stripped_emotion != "":

                # Stripped-Reduction-Input
                input_stripped_reduction = self.get_input('Stripped Reduction')
                # Valenz-Input
                input_valence = self.get_input('Valence', allowed_inputs=self.valence_pairs.keys())

                line.emotion_word.set_emotion_stripped(emotion=input_stripped_emotion, 
                                                       reduction=input_stripped_reduction, 
                                                       valence=input_valence)

                

            

            
        # if the input is greater than 3, we set the emotion word to the chosen-input
        else:
            matches_as_list = [item for sublist in line.matches.values() for item in sublist]
            line.emotion_word = EmotionWord(emotion=matches_as_list[eingabe-4].get_emotion(), 
                                            reduction=matches_as_list[eingabe-4].get_reduction(), 
                                            modifier=matches_as_list[eingabe-4].get_modifier(), 
                                            negation=matches_as_list[eingabe-4].get_negation())
            
        # setting the coder to the coder from the class 
        line.is_labelled = True
        line.coder = self.coder

        return line

    def get_input(self, cat_displayed: str, allowed_inputs: list[str] = None) -> str:
        '''This function asks the user for an input to a given category'''

        if allowed_inputs is None:
            allowed_inputs = []

        # the checker variable is used to determine if the user input is valid
        checker = ""
        continue_loop = True
        while continue_loop:
            
            user_input = self.ui.get_input(cat_displayed + ": ")
            self.ui.display_message("Your Input: " + user_input)

            if allowed_inputs and user_input not in allowed_inputs:
                self.ui.display_message("Your Input is not in the allowed inputs")
                self.ui.display_message("Allowed Inputs: " + ", ".join(allowed_inputs))
                continue
            
            while checker not in ["0", "1"]:
                checker = self.ui.get_input("Is this correct? (0 = No, 1 = Yes)")

                if checker not in ["0", "1"]:
                    self.ui.display_message("Please choose 0 or 1")
                    continue
                elif checker == "0":
                    user_input = self.ui.get_input(cat_displayed + ": ")
                    self.ui.display_message("Your Input: " + user_input)
                    checker = ""
                    if allowed_inputs and user_input not in allowed_inputs:
                        self.ui.display_message("Your Input is not in the allowed inputs")
                        self.ui.display_message("Allowed Inputs: " + ", ".join(allowed_inputs))
                        break
                elif checker == "1":
                    continue_loop = False
                    break
       
       

        return user_input

