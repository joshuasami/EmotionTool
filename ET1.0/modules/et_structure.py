"""This module includes all structural definitions, which are used for ET"""

from modules.io_machine import IOMachine
from typing import Iterator

class EmotionWord:
    def __init__(self, emotion: str, reduction: str, modifier: list[str] = None, negation: list[str] = None, emotion_stripped: dict = None) -> None:
        self.emotion = emotion
        self.reduction = reduction
        
        if modifier is None:
            modifier = []
        self.modifier = modifier

        if negation is None:
            negation = []
        self.negation = negation

        if emotion_stripped is None:
            emotion_stripped = {}
        self.emotion_stripped = emotion_stripped

    def __repr__(self) -> str:
        return f"EmotionWord(emotion={self.emotion}, reduction={self.reduction}, modifier={self.modifier}, negation={self.negation}, emotion_stripped={self.emotion_stripped})"
    
    def __str__(self) -> str:
        return f"Emotion: {self.emotion}, Reduction: {self.reduction}, Modifier: {', '.join(self.modifier)}, Negation: {', '.join(self.negation)}"

    def __hash__(self) -> int:
        return hash((self.emotion, self.reduction, tuple(self.modifier), tuple(self.negation)))
        

    def __eq__(self, other):
        if isinstance(other, EmotionWord):
            return (self.emotion == other.emotion and
                    self.reduction == other.reduction and
                    self.modifier == other.modifier and
                    self.negation == other.negation)
        return False
    
    def get_emotion(self) -> str:
        '''This function returns the emotion word'''
        return self.emotion

    def get_reduction(self) -> str:
        '''This function returns the reduction'''
        return self.reduction
    
    def get_modifier(self) -> list[str]:
        return self.modifier
    
    def get_negation(self) -> list[str]:
        return self.negation
    
    def get_emotion_stripped(self) -> dict:
        return self.emotion_stripped
    
    def set_emotion_stripped(self, emotion: str, reduction: str, valence: str) -> None:
        self.emotion_stripped = {'emotion':emotion, 'reduction':reduction, 'valence':valence}
    
    def get_stripped_emotion(self) -> str:
        return self.emotion_stripped['emotion']
    
    def get_stripped_reduction(self) -> str:
        return self.emotion_stripped['reduction']
    
    def get_valence(self) -> str:
        return self.emotion_stripped['valence']
    
    def set_emotion_word(self, emotion: str, reduction: str, modifier: list[str], negation: list[str]) -> None:
        self.emotion = emotion
        self.reduction = reduction
        self.modifier = modifier
        self.negation = negation
    
    def exists_stripped(self) -> bool:
        return bool(self.emotion_stripped)

class EmotionLine:
    '''This class reprents one answer of a vignette'''
    
    def __init__(self, answers: dict[str],
                 other_columns: dict[str] = None,
                 emotion_word: EmotionWord = None,
                 matches: dict = None, 
                 raised_problems: list[str] = None,
                 coder: str = "", ) -> None:
        
        
        self.answers = answers
        self.other_columns = other_columns

        if emotion_word is None:
            emotion_word = EmotionWord(emotion='', reduction='')
        self.emotion_word = emotion_word
        
        if self.emotion_word.get_emotion() != '':
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

    def __repr__(self) -> str:
        return f"EmotionLine(answers={self.answers}, other_columns={self.other_columns}, emotion_word={self.emotion_word}, matches={self.matches}, raised_problems={self.raised_problems}, coder={self.coder})"
    
    
    def update_from_other(self, other):
        self.answers = other.answers
        self.other_columns = other.other_columns
        self.emotion_word = other.emotion_word
        self.is_labelled = other.is_labelled
        self.raised_problems = other.raised_problems
        self.matches = other.matches
        self.coder = other.coder
        
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

        string_seperator = self.io.get_string_seperator() + " "

        for row in input_file_raw:
            answers = {}
            other_columns = {}
            emotion_word = {'emotion':'', 'reduction':'', 'modifier':'', 'negation':''}
            raised_problems = []
            coder = ""

            for key, value in row.items():
                if key in self.labels_to_look_through:
                    answers[key] = value
                elif key == self.et_labels['problems']:
                    raised_problems = value.split(string_seperator)
                elif key == self.et_labels['coder']:
                    coder = value
                elif key == self.et_labels['emotion']:
                    emotion_word['emotion'] = value
                elif key == self.et_labels['reduction']:
                    emotion_word['reduction'] = value
                elif key == self.et_labels['modifier']:
                    emotion_word['modifier'] = value.split(string_seperator)
                elif key == self.et_labels['negation']:
                    emotion_word['negation'] = value.split(string_seperator)
                else:
                    other_columns[key] = value

            out.append(EmotionLine(answers=answers, 
                                other_columns=other_columns, 
                                emotion_word=EmotionWord(emotion=emotion_word['emotion'], reduction=emotion_word['reduction'], modifier=emotion_word['modifier'], negation=emotion_word['negation']),
                                coder=coder,
                                raised_problems=raised_problems))

        return out

    def save_df(self) -> None:
        '''This function saves the df to the csv-file'''

        output_list = []
        string_seperator = self.io.get_string_seperator() + " "

        for line in self.df:
            tmp_out = {}

            tmp_out.update(line.answers)
            tmp_out.update(line.other_columns)
            tmp_out.update({self.et_labels['emotion']:line.emotion_word.get_emotion()})
            tmp_out.update({self.et_labels['reduction']:line.emotion_word.get_reduction()})
            tmp_out.update({self.et_labels['modifier']:string_seperator.join(line.emotion_word.get_modifier())})
            tmp_out.update({self.et_labels['negation']:string_seperator.join(line.emotion_word.get_negation())})
            tmp_out.update({self.et_labels['problems']:string_seperator.join(line.raised_problems)})
            tmp_out.update({self.et_labels['coder']:line.coder})

            output_list.append(tmp_out)
        
        # saving the df
        self.io.save_file(file_url=self.output_file_url, output_content=output_list, add_timestamp=True, filetype="csv", header_row=self.header_row)

    def iterate_rows(self) -> Iterator[EmotionLine]:
        '''This function iterates over the rows of the df'''

        return iter(self.df)

    def get_problems_count(self) -> dict[int]:

        out = {}
        out['total'] = 0
        out['lines_with_problems'] = 0

        for line in self.iterate_rows():
            out['total'] += len(line.raised_problems)
            out['lines_with_problems'] += 1 if len(line.raised_problems) > 0 else 0
            for problem in line.raised_problems:
                if problem in out:
                    out[problem] += 1
                else:
                    out[problem] = 1

        return out
    
    def get_unlabelled_count(self) -> int:
        '''This method gives you the number of unlabele'''

        out = 0

        for line in self.iterate_rows():
            out += 0 if line.is_labelled else 1

        return out

class Wordlist:
    '''This class stores the three wordlists'''

    def __init__(self, io: IOMachine, wordlist_labels: dict[str], emotions_dict_url: str, modifier_dict_url: str, negations_dict_url: str) -> None:
        
        self.io = io

        self.wordlist_labels = wordlist_labels

        self.emotion_dict = {}
        self.negations = []
        self.modifiers = []

        self.emotion_dict_url = emotions_dict_url
        self.load_emotion_dict(self.emotion_dict_url)

        self.modifier_dict_url = modifier_dict_url
        self.load_modifiers(self.modifier_dict_url)

        self.negations_dict_url = negations_dict_url
        self.load_negations(self.negations_dict_url)

    def get_emotions(self) -> list:
        '''This function returns all emotions'''

        return list(self.emotion_dict.keys())
    
    def get_negations(self) -> list:
        '''This function returns all negations'''

        return self.negations
    
    def get_modifiers(self) -> list:
        '''This function returns all modifiers'''

        return self.modifiers

    def is_emotion(self, word: str) -> bool:
       '''This function checks if a word is an emotion. For this it looks into the emotion_dict'''

       return word in self.emotion_dict
        
    def is_negation(self, word: str) -> bool:
        '''This function checks if a word is a negation. For this it looks into the negations-list'''

        return word in self.negations
        
    def is_modifier(self, word: str) -> bool:
        '''This function checks if a word is an modifier. For this it looks into the modifiers-list'''
        
        return word in self.modifiers
        
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
    
    def add_modifier(self, modifier: str) -> None:
        '''This function adds an modifier to the modifiers-list'''

        self.modifiers.append(modifier)

    def load_emotion_dict(self, emotion_dict_url: str) -> bool:
        '''This function converts the input dict into a list for a single word list'''
        try:
            emotion_dict_raw = self.io.load_file(emotion_dict_url)

            out = {}

            for row in emotion_dict_raw:
                emotion = row[self.wordlist_labels['emotion']]
                reduction = row[self.wordlist_labels['reduction']]
                valence = row[self.wordlist_labels['valence']]
                out[emotion] = {'reduction': reduction, 'valence': valence}

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

    def load_modifiers(self, modifier_dict_url: str) -> bool:
        '''This function converts the input dict into a list for a single word list'''
        
        try:
            self.modifiers = self.load_single_list(modifier_dict_url)
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
            tmp_out = {self.wordlist_labels['emotion']:key}
            for k,v in value.items():
                tmp_out.update({self.wordlist_labels[k]:v})
            out.append(tmp_out)

        self.io.save_file(file_url=self.emotion_dict_url, output_content=out)
    
    def save_negations(self) -> None:
        '''This function converts the input dict into a list for a single word list'''
        
        out = []

        for negation in self.negations:
            out.append({self.wordlist_labels['negation']:negation})

        self.io.save_file(file_url=self.negations_dict_url, output_content=out)

    def save_modifiers(self) -> None:
        '''This function converts the input dict into a list for a single word list'''
        
        out = []

        for modifier in self.modifiers:
            out.append({self.wordlist_labels['modifier']:modifier})

        self.io.save_file(file_url=self.modifier_dict_url, output_content=out)

    def save_wordlists(self) -> None:
        '''This function converts the input dict into a list for a single word list'''
        
        self.save_emotion_dict()
        self.save_negations()
        self.save_modifiers()