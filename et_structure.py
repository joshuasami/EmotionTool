"""This module includes all structural definitions, which are used for ET"""


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

        
        if raised_problems is None:
            raised_problems = []
        self.raised_problems = raised_problems

        if matches is None:
            matches = {}
        self.matches = matches

        self.coder = coder
        