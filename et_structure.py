"""This module includes all structural definitions, which are used for ET"""

class EmoWord:
    '''Class which holds one emotion word and its connections'''

    def __init__(self, emotion: str = "", reduction: str = "", modifier: str  = "", negation: str  = ""):
        self.emotion = emotion
        self.reduction = reduction
        self.modifier = modifier
        self.negation = negation

    def get_emotion(self) -> str:
        '''Function that returns the emotion'''

        return self.emotion
    
    def get_reduction(self) -> str:
        '''Function that returns the reduction'''

        return self.reduction
    
    def get_modifier(self) -> str:
        '''Function that returns the modifier'''
        
        return self.modifier
    
    def get_negation(self) -> str:
        '''Function that returns the negation'''
        
        return self.negation
    
    def set_emotion(self, emotion: str):
        '''Function that sets the emotion'''
        
        self.emotion = emotion
    
    def set_reduction(self, reduction: str):
        '''Function that sets the reduction'''

        self.reduction = reduction

    def set_modifier(self, modifier: str):
        '''Function that sets the modifier'''

        self.modifier = modifier

    def set_negation(self, negation: str):
        '''Function that sets the negation'''

        self.negation = negation


class EmotionLine:
    '''This class reprents one answer of a vignette'''
    
    def __init__(self, answers: dict, other_columns: dict, matches: list = None, raised_problem: int = None) -> None:
        self.answers = answers
        self.other_columns = other_columns
        self.raised_problem = raised_problem

        if matches is None:
            matches = []
        self.matches = matches
    
    def get_answers(self) -> dict:
        '''Function that returns the answers'''

        return self.answers

    def get_other_columns(self) -> dict:
        '''Function that returns the other columns'''

        return self.other_columns



class ET:

    def checkLine(self, line: str) -> list:
        test = line


class DataFrame:
    def __init__(self, file: str):
      self.file = file
      

      

