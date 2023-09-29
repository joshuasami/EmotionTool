'''This module opens and saves files. Supported Filetypes: .csv and .json'''

import csv
import json
import re
import sys
from time import gmtime, strftime

class IOMachine:
    '''Class to load and save files'''
    
    def __init__(self, encoding: str, delimiter: str):
        self.encoding = encoding
        self.delimiter = delimiter

    def load_file(self, file: str, filetype: str = None, encoding: str = None, delimiter: str = None) -> dict:
        '''General Method to call, if you want to open a file.
        The Function will call any needed functions for different file-formats.'''
         # if no encoding was given as a parameter, the encoding is set to the class variable
        if encoding is None:
            encoding = self.encoding
        
        # if no delimiter was given as a parameter, the encoding is set to the class variable
        if delimiter is None:
            delimiter = self.delimiter
        
        if filetype is None:
            filetype = re.search(r'\.([^.]+)$', file).group(1)

        if filetype == "csv":
            return self.load_csv(file, encoding, delimiter)
        
        elif filetype == "json":
            return self.load_json(file, encoding)
        
        else:
            print(f"The filetype .{filetype} is not supported yet")
            sys.exit()

    def load_json(self, file: str, encoding: str) -> dict:
        '''Method to load Json-Files'''
        
        # opening json-File
        with open(file, encoding=encoding) as jsonfile:
            out = json.load(jsonfile)

        return out
    
    def load_csv(self, file: str, encoding: str, delimiter: str) -> dict:
        '''Method to load CSV-Files. The output is put into a list of Dictionaries.'''
        out = {}
        row_categories = {}

        # opening csv-File
        with open(file, encoding=encoding) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
            
            
            # iterating over rows
            for count_nr, row in enumerate(csv_reader):
                if count_nr > 0:
                    out[count_nr] = {}

                # iterating over cells inside of row
                for i, cell in enumerate(row):
                    
                    if count_nr == 0:
                        row_categories[i] = cell
                        
                    else:
                        out[count_nr][row_categories[i]] = cell

        return out
    
    def save_file(self, file: str, output, encoding: str = None, delimiter: str = None):
        '''General Method to call, if you want to save a file.
        The Function will call any needed functions for different file-formats.'''
         # if no encoding was given as a parameter, the encoding is set to the class variable
        if encoding is None:
            encoding = self.encoding
        
        # if no delimiter was given as a parameter, the encoding is set to the class variable
        if delimiter is None:
            delimiter = self.delimiter
        
        # creating backup of data
        timestamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        backup_name = f"{file}_backup_{timestamp}"
        with open(backup_name, "w", encoding=encoding) as f:
            f.write(output)

        
        return file

class Communicator:
    def __init__(self) -> None:
        pass 