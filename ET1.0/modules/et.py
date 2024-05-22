'''This module contains the ET class, which is used to analyze sentences for emotion terms.'''

import re
from modules.et_structure import EmotionLine, Wordlist, EmotionWord

class ET:
    '''ET can, equipt with an emotion, modifier and reduction list, analyze sentences for emotion terms '''

    def __init__(self, wordlist: Wordlist, valence_pairs: dict[str], labels_raising_problem: list[str] = None) -> None:
        
        self.wordlist = wordlist

        self.valence_pairs = valence_pairs

        if labels_raising_problem is None:
            labels_raising_problem = []
        self.labels_raising_problem = labels_raising_problem

    def check_line(self, line: EmotionLine, labels_raising_problem: list = None) -> EmotionLine:
        '''This function checks a single line for emotion terms and its connected modifiers and negations'''

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
            if "3" not in line.raised_problems:
                line.raised_problems.append("3")
            return line

        # append error code 2, if there was more than one match found
        if counter > 1:
            if "2" not in line.raised_problems:
                line.raised_problems.append("2")

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
                if len(match.get_negation()) > 1:
                    multiple_negations = True
                if match.get_reduction() == "":
                    no_reduction = True      

        # here is checked, if all the matches are exactly the same
        all_matches = [match for matches in line.matches.values() for match in matches]
        all_matches_same = all(match == all_matches[0] for match in all_matches)

        if all_matches_same:
            if "2" in line.raised_problems:
                line.raised_problems.remove("2")
                counter = 1
                 

        # append error code 1, if there was a match with no reduction
        if no_reduction and "1" not in line.raised_problems:
            line.raised_problems.append("1")
        


        # append error code 0, if there was a match in a column, which was marked to raise errors
        if label_raising_problem and "0" not in line.raised_problems:
            line.raised_problems.append("0")

        if all_matches_same and other_than_label_raising_problem and "0" in line.raised_problems:
            line.raised_problems.remove("0")

        # append error code 4, if there was more than one negation found
        if multiple_negations and "4" not in line.raised_problems:
            line.raised_problems.append("4")


        # if there are no problems and one found match, then the emotion word is set
        if len(line.raised_problems) == 0 and counter == 1:
            line.emotion_word = list(line.matches.values())[0][0]
            line.is_labelled = True

            # setting the last person coding to ET
            line.coder = "ET"

        return line

    def check_for_emotion(self, line: str) -> list[dict]:
        '''This function is the main method of ET
        if presented with a sentence in string format, it analyzes it for used emotions and its connected modifiers and negations'''
        
        # the input line is converted into a list of words and empty list for the rest of the line is created
        line = self.str2list(line)
        line_rest = []
        
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
            found_modifier = []
            found_negation = []
            found_post_modifier = []
            found_post_negation = []


            line, found_emotion = self.get_longest_match(line, self.wordlist.get_emotions())
            if found_emotion == "":
                line_rest.insert(0,line[-1])
                line = line[:-1]
                continue

            # here happens the same for modifiers, what already happend for the emotion terms
            # it works almost the same. the only difference is, that there can be multiple modifiers in a row
            # e.g. "sehr sehr sehr"
            line, found_modifier = self.find_matches(line, self.wordlist.get_modifiers())
            line, found_negation = self.find_matches(line, self.wordlist.get_negations())

            line_rest, found_post_negation = self.find_matches(line_rest, self.wordlist.get_negations(), start_from_beginning=True)
            line_rest, found_post_modifier = self.find_matches(line_rest, self.wordlist.get_modifiers(), start_from_beginning=True)
            split_emotion = self.str2list(found_emotion)
            split_emotion, extra_found_modifier = self.find_matches(split_emotion, self.wordlist.get_modifiers(), remove_unmatched=True)

            split_emotion = self.str2list(found_emotion)
            split_emotion, extra_found_negation = self.find_matches(split_emotion, self.wordlist.get_negations(), remove_unmatched=True)
            
            
            # if there was a negation found, the reduction is set to the opposite of the reduction connected to the found emotion
        
            if len(found_negation) + len(found_post_negation) == 1:
                try:
                    found_reduction = self.valence_pairs[self.wordlist.get_valence(found_emotion)]
                except KeyError:
                    found_reduction = ''
            

            elif len(found_negation) + len(found_post_negation) == 0:
                # the reduction connected to the found emotion is saved
                found_reduction = self.wordlist.get_reduction(found_emotion)

            else:
                found_reduction = ''

            
            found_emotion = ' '.join(found_negation + found_modifier + [found_emotion] + found_post_negation + found_post_modifier)
            
            if extra_found_modifier:
                found_modifier = extra_found_modifier + found_modifier

            if extra_found_negation:
                found_negation = extra_found_negation + found_negation

            if found_post_modifier:
                found_modifier = found_modifier + found_post_modifier

            if found_post_negation:
                found_negation = found_negation + found_post_negation

            # the found emotion, reduction, modifier and negation are saved in a dict and appended to the output list
            out.append(
                EmotionWord(emotion=found_emotion,
                            reduction=found_reduction,
                            modifier=found_modifier,
                            negation=found_negation
                            )
            )
            
        return out
    
    def find_matches(self, line, wordlist, remove_unmatched=False, start_from_beginning=False):
        # Initialize an empty list to store the matches
        matches_tmp = []
        while len(line) > 0:
            line, found_tmp = self.get_longest_match(line, wordlist, start_from_beginning)
            
            if found_tmp == "":
                if remove_unmatched:
                    line = line[1:] if start_from_beginning else line[:-1]
                    continue
                else:
                    
                    break
            else:
                matches_tmp.append(found_tmp) if start_from_beginning else matches_tmp.insert(0, found_tmp)
        return line, matches_tmp
    
    def get_longest_match(self, line: list[str], wordlist: list, start_from_beginning=False) -> (list[str],str):
        '''This function is used to find the longest match of a wordlist in a line'''

        # all entries in the emotion wordlist are looked for in the input line
        # the key is here, that we start at the end of the line
        out = ''
        matches = {}
        for entry in wordlist:

            # the emotion is converted into a list of words
            split_entry = self.str2list(entry)
            try:
                if start_from_beginning:
                    if line[:len(split_entry)] == split_entry:
                        matches[entry] = split_entry
                else:
                    if line[-len(split_entry):] == split_entry:
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
        key_with_longest_value = ''

        for key_match, split_match in matches.items():
            if len(split_match) > len(longest_value):
                longest_value = split_match
                key_with_longest_value = key_match
        
        out = key_with_longest_value

        # the found emotion is deleted from the inputline-list
        if start_from_beginning:
            line = line[len(longest_value):]
        else:
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