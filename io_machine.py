'''This module opens and saves files. Supported Filetypes: .csv and .json'''

import csv
import json
import re
from functions import exit_programm
from user_interface import UserInterface


class IOMachine:
    '''Class to load and save files'''
    
    def __init__(self, encoding: str, delimiter: str, ui: UserInterface):
        self.encoding = encoding
        self.delimiter = delimiter
        self.ui = ui

    def load_file(self, file: str, filetype: str = None) -> dict|list:
        '''General Method to call, if you want to open a file.
        The Function will call any needed functions for different file-formats.'''
        
        if filetype is None:
            filetype = re.search(r'\.([^.]+)$', file).group(1)

        if filetype == "csv":
            return self.load_csv(file=file, encoding=self.encoding, delimiter=self.delimiter)
        
        elif filetype == "json":
            return self.load_json(file, self.encoding)
        
        else:
            self.ui.display_message(f"The filetype .{filetype} is not supported yet")
            exit_programm()

    def load_json(self, file: str, encoding: str) -> dict:
        '''Method to load Json-Files'''
        
        try:
            # opening json-File
            with open(file, encoding=encoding, newline='') as jsonfile:
                out = json.load(jsonfile)
        except Exception as error:
            self.ui.display_message(f"The json-file {file} couldn't be loaded.")
            self.ui.display_message(error)
            exit_programm()
        return out
    
    def load_csv(self, file: str, encoding: str, delimiter: str) -> list:
        '''Method to load CSV-Files. The output is put into a list of Dictionaries.'''
        
        out = []
        
        try:
            # opening csv-File
            with open(file, encoding=encoding, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
                out = list(csv_reader)
        except Exception as error:
            self.ui.display_message(f"The csv-file {file} couldn't be loaded.")
            self.ui.display_message(error)
            exit_programm()
        
        if not self.check_dicts(out):
            self.ui.display_message(f"The csv-file {file} has an inhomogeneous table structure.")
            exit_programm()


        self.check_special_letters(raw_file=out, raw_file_name=file)

        return out
    
    def save_file(self, file_url: str, output_content: list|dict, filetype: str = None, header_row: list[str] = None) -> None:
        '''General Method to call, if you want to save a file.
        The Function will call any needed functions for different file-formats.'''
         # if no encoding was given as a parameter, the encoding is set to the class variable


        if filetype is None:
            filetype = re.search(r'\.([^.]+)$', file_url).group(1)

        if filetype == "csv":
            self.save_csv(file=file_url, output_content=output_content, header_row=header_row, encoding=self.encoding, delimiter=self.delimiter)
        
        elif filetype == "json":
            self.save_json(file_url, output_content, self.encoding)
        
        else:
            self.ui.display_message(f"The filetype .{filetype} is not supported yet")
            exit_programm()
    
    def save_json(self, file: str, output_content: dict, encoding: str) -> None:
        '''Method to save Json-Files'''
        try:
            # opening json-File
            with open(file, "w", encoding=encoding, newline='') as jsonfile:
                json.dump(output_content, jsonfile, indent=4)
        except Exception as error:
            self.ui.display_message(f"The json-file {file} couldn't be saved.")
            self.ui.display_message(error)
            exit_programm()
    
    def save_csv(self, file: str, output_content: list, header_row: list, encoding: str, delimiter: str) -> None:

        '''Method to save CSV-Files. The input has to be a list of Dictionaries.'''
        
        try:
            if header_row is None:
                header_row = output_content[0].keys()

            # opening and writing csv-File
            with open(file, "w", encoding=encoding, newline='') as csvfile:
                csv_writer = csv.DictWriter(csvfile, delimiter=delimiter, fieldnames=header_row)
                csv_writer.writeheader()
                csv_writer.writerows(output_content)
        except Exception as error:
            self.ui.display_message(f"The csv-file {file} couldn't be saved.")
            self.ui.display_message(error)
            exit_programm()

    def get_csv_header(self, file: str) -> list:
        '''Method to get the header row of a csv file'''
        

        try:
            with open(file, encoding=self.encoding, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile, delimiter=self.delimiter)
                header_row = csv_reader.fieldnames
        except Exception as error:
            self.ui.display_message(f"The csv-file {file} couldn't be loaded.")
            self.ui.display_message(error)
            exit_programm()
            
        return header_row
    
    def check_dicts(self, list_of_dicts) -> bool:
        '''This function checks if the dicts in a list have the same keys and the same length'''
        
        # check if the list is empty
        if not list_of_dicts:
            return False
        
        # get header row and length of first dict
        first_dict_keys = set(list_of_dicts[0].keys())
        first_dict_length = len(list_of_dicts[0])

        for d in list_of_dicts:
            # check if the keys and the length of the dicts are the same
            if set(d.keys()) != first_dict_keys or len(d) != first_dict_length:
                return False

        return True
    
    def check_special_letters(self, raw_file: dict, raw_file_name: str) -> None:
        """Checks if the raw-file contains special letters, which are than displayed, so the user can check if their were laoded correctly."""

        pattern = re.compile(r"[^A-Za-z0-9\s_\-,#.:]")  # Regex-Muster für nicht erlaubte Zeichen


        for line in raw_file:
            found_special_letter = False
            for value in line.values():
                
                # Prüfen, ob der Satz nicht erlaubte Zeichen enthält
                if re.search(pattern, value):
                    found_special_letter = True

            if found_special_letter:
                self.ui.display_message(f"Example for {raw_file_name}:\n")
                self.ui.dict_dict_as_table(line)
                self.ui.display_message("\n")
                return None
