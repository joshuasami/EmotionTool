'''This module contains the ET class, which is used to analyze sentences for emotion terms.'''

import re
from et_structure import EmotionLine

class ET:
    '''ET can, equipt with an emotion, modifier and reduction list, analyze sentences for emotion terms '''

    def __init__(self, emotion_dict: dict, intensifiers: list, negations: list, answer_columns: list = None, labels_raising_problem: list = None) -> None:
        self.emotion_dict = emotion_dict
        self.intensifiers = intensifiers
        self.negations = negations

        if answer_columns is None:
            answer_columns = []
        self.answer_columns = answer_columns

        if labels_raising_problem is None:
            labels_raising_problem = []
        self.labels_raising_problem = labels_raising_problem


    def check_line(self, line: EmotionLine, labels_raising_problem: list = None) -> EmotionLine:
        '''This function checks a single line for emotion terms and its connected intensifiers and negations'''

        # explanation of raised problem-codes
        # 0 = match in marked column
        # 1 = no reduction
        # 2 = over 1
        # 3 = 0 matches

        if labels_raising_problem is None:
            labels_raising_problem = self.labels_raising_problem

        # all columns, which are marked to be checked, are checked for emotion terms
        for key, col in line.answers.items():

            tmp_checked = self.check_for_emotion(col)

            # if there were matches found, they are saved in the line
            if tmp_checked:

                # if there is no entry for the column in the matches dict, it is created
                if key in line.matches:
                    line.matches[key].extend(tmp_checked)
                else:
                    line.matches[key] = tmp_checked

        # the number of matches is counted
        counter = 0
        for value in line.matches.values():
            counter += len(value)

        # append error-code 3, if there were no matches found
        if counter == 0:
            if 3 not in line.raised_problems:
                line.raised_problems.append(3)
            return line

        # append error code 2, if there was more than one match found
        if counter > 1:
            if 2 not in line.raised_problems:
                line.raised_problems.append(2)

        # check if there was a match with no reduction or a match in a column, which was marked to raise errors
        no_reduction = False
        label_raising_problem = False
        for col, matches in line.matches.items():

            # check if the column is marked to raise errors
            if col in labels_raising_problem:
                label_raising_problem = True

            # check if there is a match with no reduction
            for match in matches:
                if match['reduction'] == "":
                    no_reduction = True             

        # append error code 1, if there was a match with no reduction
        if no_reduction and 1 not in line.raised_problems:
            line.raised_problems.append(1)

        # append error code 0, if there was a match in a column, which was marked to raise errors
        if label_raising_problem and 0 not in line.raised_problems:
            line.raised_problems.append(0)

        # if there are no problems and one found match, then the emotion word is set
        if len(line.raised_problems) == 0 and counter == 1:
            line.emotion_word = list(line.matches.values())[0][0]

            # setting the last person coding to ET
            line.coder = "ET"




        return line

    def check_for_emotion(self, line: str) -> list:
        '''This function is the main method of ET
        if presented with a sentence in string format, it analyzes it for used emotions and its connected intensifiers and negations'''
        
        # the input line is converted into a list of words
        line = self.str2list(line)
        
        # exits, if the line is empty
        if not line:
            return []

        # the output list is created
        out = []

        # everytime a value is found, its deleted from the list of the input line
        # when the line is empty, the loop is exited
        while len(line) > 0:

            # all entries in the emotion wordlist are looked for in the input line
            # the key is here, that we start at the end of the line
            matches = {}
            for emotion in self.emotion_dict.keys():

                # the emotion is converted into a list of words
                split_emotion = self.str2list(emotion)
                try:
                    # if the last words of the input line are the same as the emotion, the emotion is saved
                    if line[-len(split_emotion):len(line)] == split_emotion:
                        matches[emotion] = split_emotion
                except IndexError:
                    continue
            
            # if nothing was found, the last element of the inputline-list is deleted and a new round is started
            if not matches:
                line = line[:-1]
                continue
            
            # all the matches are checked for the longest one
            # there can be multiple matches, because one entrie can be part of another
            # e.g. "Lust" and "keine Lust" can both be found. But because we check for the longest match, only "keine Lust" is used
            longest_value = ''
            key_with_longest_value = None

            for key_match, split_match in matches.items():
                if len(split_match) > len(longest_value):
                    longest_value = split_match
                    key_with_longest_value = key_match
            
            found_emotion = key_with_longest_value

            # the reduction connected to the found emotion is saved
            found_reduction = self.emotion_dict[found_emotion]

            # the found emotion is deleted from the inputline-list
            line = line[:-len(longest_value)]
            
            # here happens the same for intensifiers, what already happend for the emotion terms
            # it works almost the same. the only difference is, that there can be multiple intensifiers in a row
            # e.g. "sehr sehr sehr"
            matches_tmp = []

            while len(line)>0:

                matches = {}

                for intensifier in self.intensifiers:
                    split_intensifier = self.str2list(intensifier)
                    try:
                        if line[-len(split_intensifier):len(line)] == split_intensifier:
                            matches[intensifier] = split_intensifier
                    except IndexError:
                        continue

                if not matches:
                    break
                

                longest_value = ''
                key_with_longest_value = None

                for key_match, split_match in matches.items():
                    if len(split_match) > len(longest_value):
                        longest_value = split_match
                        key_with_longest_value = key_match
                
                line = line[:-len(longest_value)]
                matches_tmp.insert(0,key_with_longest_value)

            found_intensifier = matches_tmp

            # here happens the same for negations, like for intensifiers. it's working in an identical-way
            matches_tmp = []

            while len(line)>0:

                matches = {}

                for negation in self.negations:
                    split_negation = self.str2list(negation)
                    try:
                        if line[-len(split_negation):len(line)] == split_negation:
                            matches[negation] = split_negation
                    except IndexError:
                        continue

                if not matches:
                    break

                longest_value = ''
                key_with_longest_value = None

                for key_match, split_match in matches.items():
                    if len(split_match) > len(longest_value):
                        longest_value = split_match
                        key_with_longest_value = key_match
                
                line = line[:-len(longest_value)]
                matches_tmp.insert(0,key_with_longest_value)


            found_negation = matches_tmp
            
            out.append(
                {'emotion':found_emotion,
                 'reduction':found_reduction,
                 'intensifier':' '.join(found_intensifier),
                 'negation':' '.join(found_negation)
                 })
        
        return out
    
    def str2list(self,s: str) -> list:
        '''This Method is used to clean strings and return them in a list format.'''
        
        # removes whitespace at ends
        s = s.strip()

        # reduces multiple whitespaces to one
        s = re.sub(" +", " ", s)

        # only keep letter, numbers and spaces
        s = re.sub("[^\\w\\d\\s]","",s)

        # this puts all letters into lowercase
        s = s.lower()

        # splits string into list of words, based on whitespaces
        out = s.split()

        # returns list of words
        return out