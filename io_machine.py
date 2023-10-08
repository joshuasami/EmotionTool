'''This module opens and saves files. Supported Filetypes: .csv and .json'''

import csv
import json
import re
import sys
from time import gmtime, strftime
from functions import *

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
            exit_programm()

    def load_json(self, file: str, encoding: str) -> dict:
        '''Method to load Json-Files'''
        
        # opening json-File
        with open(file, encoding=encoding) as jsonfile:
            out = json.load(jsonfile)

        return out
    
    def load_csv(self, file: str, encoding: str, delimiter: str) -> list:
        '''Method to load CSV-Files. The output is put into a list of Dictionaries.'''
        
        out = []

        # opening csv-File
        with open(file, encoding=encoding) as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
            out = list(csv_reader)
            
        return out
    
    def save_file(self, file: str, output_content: list|dict, filetype: str = None, header_row: list[str] = None, encoding: str = None, delimiter: str = None) -> None:
        '''General Method to call, if you want to save a file.
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
            self.save_csv(file=file, output_content=output_content, header_row=header_row, encoding=encoding, delimiter=delimiter)
        
        elif filetype == "json":
            self.save_json(file, output_content, encoding)
        
        else:
            print(f"The filetype .{filetype} is not supported yet")
            exit_programm()
    
    def save_json(self, file: str, output_content: dict, encoding: str) -> None:
        '''Method to save Json-Files'''
        
        # opening json-File
        with open(file, "w", encoding=encoding) as jsonfile:
            json.dump(output_content, jsonfile, indent=4)
    
    def save_csv(self, file: str, output_content: list, header_row: list, encoding: str, delimiter: str) -> None:

        '''Method to save CSV-Files. The input has to be a list of Dictionaries.'''
        

        if header_row is None:
            header_row = output_content[0].keys()

        # opening and writing csv-File
        with open(file, "w", encoding=encoding) as csvfile:
            csv_writer = csv.DictWriter(csvfile, delimiter=delimiter, fieldnames=header_row)
            csv_writer.writeheader()
            csv_writer.writerows(output_content)

    def get_csv_header(self, file: str, encoding: str = None, delimiter: str = None) -> list:
        '''Method to get the header row of a csv file'''
        
        # if no encoding was given as a parameter, the encoding is set to the class variable
        if encoding is None:
            encoding = self.encoding

        # if no delimiter was given as a parameter, the encoding is set to the class variable
        if delimiter is None:
            delimiter = self.delimiter

        with open(file, encoding=encoding) as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
            header_row = csv_reader.fieldnames

        return header_row