import re
from et_structure import EmotionLine
from et_str2list import str2list

class ET:
    '''ET can, equipt with an emotion, modifier and reduction list, analyze sentences for emotion terms '''
    def __init__(self, emotion_dict: dict, intensifiers: list, negations: list, answer_columns: list = None, first_ignore: bool = True) -> None:
        self.emotion_dict = emotion_dict
        self.intensifiers = intensifiers
        self.negations = negations
        self.answer_columns = answer_columns
        self.first_ignore = first_ignore

    def check_line(self, line: EmotionLine) -> EmotionLine:

        if line.matches is not None:
            return line
        
        matches = []

        for key, col in line.anwers.items():
            matches.append({key:self.check_line(col)})



    def check_for_emotion(self, line: str) -> list:
        '''This function is the main method of ET
        if presented with a sentence in string format, it analyzes it for used emotions and its connected intensifiers and negations'''
        
        line = str2list(line)

        if not line:
            return [["","",[],[]]]

        out = []

        while len(line) > 0:

            matches = {}

            for emotion in self.emotion_dict.keys():
                split_emotion = str2list(emotion)
                try:
                    if line[-len(split_emotion):len(line)] == split_emotion:
                        matches[emotion] = split_emotion
                except IndexError:
                    continue

            if not matches:
                line = line[:-1]
                continue
            
            longest_value = ''
            key_with_longest_value = None

            for key_match, split_match in matches.items():
                if len(split_match) > len(longest_value):
                    longest_value = split_match
                    key_with_longest_value = key_match
            
            found_emotion = key_with_longest_value

            found_reduction = self.emotion_dict[found_emotion]

            line = line[:-len(longest_value)]
            
            matches_tmp = []

            while len(line)>0:

                matches = {}

                for intensifier in self.intensifiers:
                    split_intensifier = str2list(intensifier)
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

            matches_tmp = []

            while len(line)>0:

                matches = {}

                for negation in self.negations:
                    split_negation = str2list(negation)
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
            
            out.append([found_emotion,found_reduction, found_intensifier,found_negation])
        
        return out