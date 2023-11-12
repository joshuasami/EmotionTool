"""This module includes all structural definitions, which are used for ET"""

from io_machine import IOMachine
from typing import Iterator

class EmotionWord:
    def __init__(self, emotion: str, reduction: str, intensifier: list[str] = None, negation: list[str] = None) -> None:
        self.emotion = emotion
        self.reduction = reduction
        
        if intensifier is None:
            intensifier = []
        self.intensifier = intensifier

        if negation is None:
            negation = []
        self.negation = negation

    def __str__(self) -> str:
        return f"EmotionWord(emotion={self.emotion}, reduction={self.reduction}, intensifier={self.intensifier}, negation={self.negation})"
    
    def get_intensifier_string(self) -> str:
        return ', '.join(self.intensifier)
    
    def get_negation_string(self) -> str:
        return ', '.join(self.negation)


class EmotionLine:
    '''This class reprents one answer of a vignette'''
    
    def __init__(self, answers: dict,
                 other_columns: dict = None,
                 emotion_word: dict = None,
                 matches: dict = None, 
                 raised_problems: list = None,
                 coder: str = "", ) -> None:
        
        
        self.answers = answers
        self.other_columns = other_columns

        if emotion_word is None:
            emotion_word = {}
        self.emotion_word = emotion_word
        
        if 'emotion' in self.emotion_word.keys() and self.emotion_word['emotion'] != '':
            self.is_labelled = True
        else:
            self.is_labelled = False

        
        if raised_problems is None:
            raised_problems = []
        self.raised_problems = raised_problems

        if matches is None:
            matches = {}
        self.matches = matches

        self.coder = coder
        
class DataFrame:
    '''This class stores a dataframe of ET answers'''

    def __init__(self, input_file_url: str, output_file_url: str, io: IOMachine, labels_to_look_through: list[str], et_labels: dict[str]) -> None:
        
        self.input_file_url = input_file_url
        self.output_file_url = output_file_url
        self.io = io
        self.labels_to_look_through = labels_to_look_through
        self.et_labels = et_labels

        self.header_row = self.io.get_csv_header(self.input_file_url)
        
        # adding the ET_LABELS to the header_row, if they aren't already in there
        for col in self.et_labels.values():
            if col not in self.header_row:
                self.header_row.append(col)


        self.df = self.load_df()

    def load_df(self) -> list[EmotionLine]:
        '''This function converts the input file, which is to be look through with ET and EC, into the right format'''

        try:
            input_file_raw = self.io.load_file(self.input_file_url)
        except:
            return False
        

        out = []

        for row in input_file_raw:
            answers = {}
            other_columns = {}
            emotion_word = {'emotion':'', 'reduction':'', 'intensifier':'', 'negation':''}
            raised_problems = []
            coder = ""

            for key, value in row.items():
                if key in self.labels_to_look_through:
                    answers[key] = value
                elif key == self.et_labels['problems']:
                    raised_problems = [int(i) for i in value.split()]
                elif key == self.et_labels['coder']:
                    coder = value
                elif key == self.et_labels['emotion']:
                    emotion_word['emotion'] = value
                elif key == self.et_labels['reduction']:
                    emotion_word['reduction'] = value
                elif key == self.et_labels['intensifier']:
                    emotion_word['intensifier'] = value.split(', ')
                elif key == self.et_labels['negation']:
                    emotion_word['negation'] = value.split(', ')
                else:
                    other_columns[key] = value

            out.append(EmotionLine(answers=answers, 
                                other_columns=other_columns, 
                                emotion_word=emotion_word, 
                                coder=coder,
                                raised_problems=raised_problems))

        return out

    def save_df(self) -> None:
        '''This function saves the df to the csv-file'''

        output_list = []

        for line in self.df:
            tmp_out = {}

            tmp_out.update(line.answers)
            tmp_out.update(line.other_columns)
            tmp_out.update({self.et_labels['emotion']:line.emotion_word['emotion']})
            tmp_out.update({self.et_labels['reduction']:line.emotion_word['reduction']})
            tmp_out.update({self.et_labels['intensifier']:', '.join(line.emotion_word['intensifier'])})
            tmp_out.update({self.et_labels['negation']:', '.join(line.emotion_word['negation'])})
            tmp_out.update({self.et_labels['problems']:' '.join([str(p) for p in line.raised_problems])})
            tmp_out.update({self.et_labels['coder']:line.coder})

            output_list.append(tmp_out)
        
        # saving the df
        self.io.save_file(file_url=self.output_file_url, output_content=output_list, filetype="csv", header_row=self.header_row)

    def iterate_rows(self) -> Iterator[EmotionLine]:
        '''This function iterates over the rows of the df'''

        return iter(self.df)

class Wordlist:
    '''This class stores the three wordlists'''

    def __init__(self, io: IOMachine, emotions_dict_url: str, intensifier_dict_url: str, negations_dict_url: str) -> None:
        
        self.io = io

        self.emotion_dict = {}
        self.negations = []
        self.intensifiers = []

        self.emotion_dict_url = emotions_dict_url
        self.load_emotion_dict(self.emotion_dict_url)

        self.intensifier_dict_url = intensifier_dict_url
        self.load_intensifiers(self.intensifier_dict_url)

        self.negations_dict_url = negations_dict_url
        self.load_negations(self.negations_dict_url)

    def get_emotions(self) -> list:
        '''This function returns all emotions'''

        return list(self.emotion_dict.keys())
    
    def get_negations(self) -> list:
        '''This function returns all negations'''

        return self.negations
    
    def get_intensifiers(self) -> list:
        '''This function returns all intensifiers'''

        return self.intensifiers

    def is_emotion(self, word: str) -> bool:
       '''This function checks if a word is an emotion. For this it looks into the emotion_dict'''

       return word in self.emotion_dict
        
    def is_negation(self, word: str) -> bool:
        '''This function checks if a word is a negation. For this it looks into the negations-list'''

        return word in self.negations
        
    def is_intensifier(self, word: str) -> bool:
        '''This function checks if a word is an intensifier. For this it looks into the intensifiers-list'''
        
        return word in self.intensifiers
        
    def get_reduction(self, word: str) -> str:
        '''This function returns the reduction of an emotion. For this it looks into the emotion_dict'''

        return self.emotion_dict[word]['reduction']

    def get_valence(self, word: str) -> str:
        '''This function returns the valence of an emotion. For this it looks into the emotion_dict'''
        
        return self.emotion_dict[word]['valence']

    def add_emotion(self, emotion: str, reduction: str, valence: str) -> None:
        '''This function adds an emotion to the emotion_dict'''

        self.emotion_dict[emotion] = {'reduction': reduction, 'valence': valence}

    def add_negation(self, negation: str) -> None:
        '''This function adds a negation to the negations-list'''

        self.negations.append(negation)
    
    def add_intensifier(self, intensifier: str) -> None:
        '''This function adds an intensifier to the intensifiers-list'''

        self.intensifiers.append(intensifier)

    def load_emotion_dict(self, emotion_dict_url: str) -> bool:
        '''This function converts the input dict into a list for a single word list'''
        try:
            emotion_dict_raw = self.io.load_file(emotion_dict_url)

            out = {}

            for row in emotion_dict_raw:
                emotion = row.pop('emotion')
                out[emotion] = row

            self.emotion_dict = out

            return True
        except:
            return False

    def load_negations(self, negations_dict_url: str) -> bool:
        '''This function converts the input dict into a list for a single word list'''
        try:
            self.negations = self.load_single_list(negations_dict_url)
            return True
        except:
            return False

    def load_intensifiers(self, intensifier_dict_url: str) -> bool:
        '''This function converts the input dict into a list for a single word list'''
        
        try:
            self.intensifiers = self.load_single_list(intensifier_dict_url)
            return True
        except:
            return False
        
    def load_single_list(self, input_list_url: str) -> list:
        '''This function converts the input dict into a list for a single word list'''    
        
        input_list = self.io.load_file(input_list_url)

        out = []

        for row in input_list:
            for word in row.values():
                out.append(word)

        return out

    def save_emotion_dict(self) -> None:
        '''This function converts the input dict into a list for a single word list'''
        
        out = []

        for key,value in self.emotion_dict.items():
            tmp_out = {'emotion':key}
            tmp_out.update(value)
            out.append(tmp_out)

        self.io.save_file(file_url=self.emotion_dict_url, output_content=out)
    
    def save_negations(self) -> None:
        '''This function converts the input dict into a list for a single word list'''
        
        out = []

        for negation in self.negations:
            out.append({'negation':negation})

        self.io.save_file(file_url=self.negations_dict_url, output_content=out)

    def save_intensifiers(self) -> None:
        '''This function converts the input dict into a list for a single word list'''
        
        out = []

        for intensifier in self.intensifiers:
            out.append({'intensifier':intensifier})

        self.io.save_file(file_url=self.intensifier_dict_url, output_content=out)

    def save_wordlists(self) -> None:
        '''This function converts the input dict into a list for a single word list'''
        
        self.save_emotion_dict()
        self.save_negations()
        self.save_intensifiers()