import csv
import json
import re

class IOMachine:
    
    def __init__(self, encoding: str, delimiter: str):
        self.encoding = encoding
        self.delimiter = delimiter

    def loadFile(self, file: str, encoding: str = None, delimiter: str = None):

         # if no encoding was given as a parameter, the encoding is set to the class variable
        if encoding == None:
            encoding = self.encoding
        
        # if no delimiter was given as a parameter, the encoding is set to the class variable
        if delimiter == None:
            delimiter = self.delimiter
        

        filetype = re.search(r'\.([^.]+)$', file).group(1)

        if filetype == "csv":
            return self.loadCsv(file, encoding, delimiter)
        
        elif filetype == "json":
            return self.loadJson(file, encoding)
        
        else:
            print("The filetype .{} is not supported yet".format(filetype))
            exit()

    def loadJson(self, file: str, encoding: str) -> dict:

        # opening json-File
        f = open(file, encoding=encoding)
        out = json.load(f)
        f.close()

        return out
    
    def loadCsv(self, file: str, encoding: str, delimiter: str) -> list:
        
        # opening json-File
        f = open(file, encoding=encoding)
        out = json.load(f)
        f.close()

        return out
    
    def saveFile(self, file: str, output, encoding: str = None, delimiter: str = None):
        
         # if no encoding was given as a parameter, the encoding is set to the class variable
        if encoding == None:
            encoding = self.encoding
        
        # if no delimiter was given as a parameter, the encoding is set to the class variable
        if delimiter == None:
            delimiter = self.delimiter
        
        test = file

    