'''This module contains the ET class, which is used to analyze sentences for emotion terms.'''

import re
from et_structure import EmotionLine
from et_structure import Wordlist

class ET:
    '''ET can, equipt with an emotion, modifier and reduction list, analyze sentences for emotion terms '''

    def __init__(self, wordlist: Wordlist, answer_columns: list = None, labels_raising_problem: list = None) -> None:
        
        self.wordlist = wordlist

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
        # 4 = more than one negations found

        if labels_raising_problem is None:
            labels_raising_problem = self.labels_raising_problem

        line.matches = {}
        line.raised_problems = []

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
        counter = sum(len(value) for value in line.matches.values())

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
        other_than_label_raising_problem = False
        multiple_negations = False
        for col, matches in line.matches.items():

            # check if the column is marked to raise errors
            if col in labels_raising_problem:
                label_raising_problem = True
            else:
                other_than_label_raising_problem = True

            # check if there is a match with no reduction
            for match in matches:
                if len(match['negation']) > 1:
                    multiple_negations = True
                if match['reduction'] == "":
                    no_reduction = True      

        # here is checked, if all the matches are exactly the same
        all_matches = [match for matches in line.matches.values() for match in matches]
        all_matches_same = all(match == all_matches[0] for match in all_matches)

        if all_matches_same:
            if 2 in line.raised_problems:
                line.raised_problems.remove(2)
                counter = 1
                 

        # append error code 1, if there was a match with no reduction
        if no_reduction and 1 not in line.raised_problems:
            line.raised_problems.append(1)
        


        # append error code 0, if there was a match in a column, which was marked to raise errors
        if label_raising_problem and 0 not in line.raised_problems:
            line.raised_problems.append(0)

        if all_matches_same and other_than_label_raising_problem and 0 in line.raised_problems:
            line.raised_problems.remove(0)

        # append error code 4, if there was more than one negation found
        if multiple_negations and 4 not in line.raised_problems:
            line.raised_problems.append(4)

        # all negations and intensifiers are joined to a string with a ", "
        '''for match in line.matches.values():
            for entry in match:
                entry['negation'] = ', '.join(entry['negation'])
                entry['intensifier'] = ', '.join(entry['intensifier'])
        '''
        
        # if there are no problems and one found match, then the emotion word is set
        if len(line.raised_problems) == 0 and counter == 1:
            line.emotion_word = list(line.matches.values())[0][0]
            line.is_labelled = True

            # setting the last person coding to ET
            line.coder = "ET"

        return line

    def check_for_emotion(self, line: str) -> list[dict]:
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

            found_emotion = ""
            found_reduction = ""
            found_intensifier = []
            found_negation = []

            line, found_emotion = self.get_longest_match(line, self.wordlist.get_emotions())
            
            if found_emotion == "":
                line = line[:-1]
                continue
            
            # here happens the same for intensifiers, what already happend for the emotion terms
            # it works almost the same. the only difference is, that there can be multiple intensifiers in a row
            # e.g. "sehr sehr sehr"
            matches_tmp = []

            while len(line)>0:

                line, found_intensifier_tmp = self.get_longest_match(line, self.wordlist.get_intensifiers())
                if found_intensifier_tmp == "":
                    break
                else:
                    matches_tmp.insert(0,found_intensifier_tmp)

            found_intensifier = matches_tmp
            
            matches_tmp = []
            split_emotion = self.str2list(found_emotion)

            while len(split_emotion) > 0:
                split_emotion, found_intensifier_tmp = self.get_longest_match(split_emotion, self.wordlist.get_intensifiers())
                if found_intensifier_tmp == "":
                    split_emotion = split_emotion[:-1]
                    continue
                else:
                    matches_tmp.insert(0,found_intensifier_tmp)
            
            extra_found_intensifier = matches_tmp

            # here happens the same for negations, like for intensifiers. it's working in an identical-way
            
            matches_tmp = []

            while len(line)>0:
                    
                line, found_negation_tmp = self.get_longest_match(line, self.wordlist.get_negations())
                if found_negation_tmp == "":
                    break
                else:
                    matches_tmp.insert(0,found_negation_tmp)

            found_negation = matches_tmp

            matches_tmp = []
            split_emotion = self.str2list(found_emotion)
            while len(split_emotion) > 0:
                split_emotion, found_negation_tmp = self.get_longest_match(split_emotion, self.wordlist.get_negations())
                if found_negation_tmp == "":
                    split_emotion = split_emotion[:-1]
                    continue
                else:
                    matches_tmp.insert(0,found_negation_tmp)

            extra_found_negation = matches_tmp
            
            
            # if there was a negation found, the reduction is set to the opposite of the reduction connected to the found emotion
        
            if len(found_negation) == 1:
                if self.wordlist.get_valence(found_emotion) == "negativ":
                    found_reduction = 'positiv'
                elif self.wordlist.get_valence(found_emotion) == "positiv":
                    found_reduction = 'negativ'
                elif self.wordlist.get_valence(found_emotion) == "neutral":
                    found_reduction = 'neutral'
            

            elif len(found_negation) == 0:
                # the reduction connected to the found emotion is saved
                found_reduction = self.wordlist.get_reduction(found_emotion)

            else:
                found_reduction = ''

            
            found_emotion = ' '.join(found_negation + found_intensifier + [found_emotion])
            
            if extra_found_intensifier:
                found_intensifier = extra_found_intensifier + found_intensifier

            if extra_found_negation:
                found_negation = extra_found_negation + found_negation

            # the found emotion, reduction, intensifier and negation are saved in a dict and appended to the output list
            out.append(
                {'emotion':found_emotion,
                 'reduction':found_reduction,
                 'intensifier':found_intensifier,
                 'negation':found_negation
                 })
        
        return out

    def get_longest_match(self, line: str, wordlist: list) -> (str,str):
        '''This function is used to find the longest match of a wordlist in a line'''

        # all entries in the emotion wordlist are looked for in the input line
        # the key is here, that we start at the end of the line
        out = ''
        matches = {}
        for entry in wordlist:

            # the emotion is converted into a list of words
            split_entry = self.str2list(entry)
            try:
                # if the last words of the input line are the same as the emotion, the emotion is saved
                if line[-len(split_entry):len(line)] == split_entry:
                    matches[entry] = split_entry
            except IndexError:
                continue
        
        # if nothing was found, the last element of the inputline-list is deleted and a new round is started
        if not matches:
            return line, out
        
        # all the matches are checked for the longest one
        # there can be multiple matches, because one entrie can be part of another
        # e.g. "Lust" and "keine Lust" can both be found. But because we check for the longest match, only "keine Lust" is used
        longest_value = ''
        key_with_longest_value = None

        for key_match, split_match in matches.items():
            if len(split_match) > len(longest_value):
                longest_value = split_match
                key_with_longest_value = key_match
        
        out = key_with_longest_value

        # the found emotion is deleted from the inputline-list
        line = line[:-len(longest_value)]

        return line, out

    def str2list(self,s: str) -> list[str]:
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