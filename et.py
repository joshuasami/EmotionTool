from io_machine import IOMachine

io = IOMachine("utf-8", ";")

class ET:
    '''ET can, equipt with an emotion, modifier and reduction list, analyze sentences for emotion terms '''
    def __init__(self, emotion_dict: dict, modifier_list: list, reduction_list: list) -> None:
        self.emotion_dict = emotion_dict
        self.modifier_list = modifier_list
        self.reduction_list = reduction_list

    def checkLine(self, line: list) -> list:
        
        
        
        pass