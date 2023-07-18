class emoword:
    def __init__(self, emotion: str = "", reduction: str = "", modifier: str  = "", negation: str  = ""):
        self.emotion = emotion
        self.reduction = reduction
        self.modifier = modifier
        self.negation = negation

    def getEmotion(self) -> str:
        return self.emotion
    
    def getReduction(self) -> str:
        return self.reduction
    
    def getModifier(self) -> str:
        return self.modifier
    
    def getNegation(self) -> str:
        return self.negation
    
    def setEmotion(self, emotion: str):
        self.emotion = emotion
    
    def setReduction(self, reduction: str):
        self.reduction = reduction

    def setModifier(self, modifier: str):
        self.modifier = modifier

    def setNegation(self, negation: str):
        self.negation = negation

    def printword(self):
        print("Emotion: " + self.emotion + ", Reduction: " + self.reduction + ", Modifier: " + self.modifier + ", Negation: " + self.negation)

class emotion_line:
    def __init__(self, answers: dict, other_columns: dict, emotion_word: emoword):
        self.answers = answers
        self.other_columns = other_columns
        self.emotion_word = emotion_word
    
    def getAnswer(self) -> dict:
        return self.answers

    def getOtherColumns(self) -> dict:
        return self.other_columns
    
    def getEmotionWord(self) -> emoword:
        return self.emotion_word
    
    def setEmotionWord(self, emotion_word: emoword):
        self.emotion_word = emotion_word

class ET:

    def checkLine(self, line: str) -> list:
        test = line


class DataFrame:
    def __init__(self, file: str):
      self.file = file
      

      

