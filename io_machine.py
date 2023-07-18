import csv

class IOMachine:
    def __init__(self, encoding: str, delimiter: str):
        self.encoding = encoding
        self.delimiter = delimiter

class CSV_IOMachine(IOMachine):
    def __init__(self, encoding: str, delimiter: str):
        super().__init__(encoding, delimiter)

    def loadFile(self, file: str, settings: dict) -> list:
        test = file

    def writeFile(self, file: str, output: list, order: list):
        test = file
    
    