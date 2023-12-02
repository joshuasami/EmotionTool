'''This module opens and saves files. Supported Filetypes: .csv and .json'''

import csv
import json
import re
import os
import shutil
from datetime import datetime

from functions import exit_programm
from user_interface import UserInterface



class IOMachine:
    '''Class to load and save files'''
    
    def __init__(self, encoding: str, delimiter: str, string_seperator: str, ui: UserInterface):
        self.encoding = encoding
        self.delimiter = delimiter
        self.string_seperator = string_seperator
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
                csv_reader = csv.DictReader((line for line in csvfile if not line.isspace()), delimiter=delimiter)
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
    
    def save_file(self, file_url: str, output_content: list|dict, add_timestamp: bool = False, filetype: str = None, header_row: list[str] = None) -> None:
        '''General Method to call, if you want to save a file.
        The Function will call any needed functions for different file-formats.'''
        
         # create directory, base and extension strings
        directory, filename = os.path.split(file_url)
        base, ext = os.path.splitext(filename)

        # create regex pattern to check if file already exists
        pattern = re.compile(f'^{re.escape(base)}{re.escape(ext)}$')
        
        # Add timestamp to filename if required and change pattern accordingly
        if add_timestamp:
            timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
            filename = f"{base}{timestamp}{ext}"
            file_url = os.path.join(directory, filename)
            pattern = re.compile(f'^{re.escape(base)}_\\d{{8}}_\\d{{6}}{re.escape(ext)}$')

        # Check if file with the same base name already exists
        for filename in os.listdir(directory):
            if pattern.match(filename):
                # Create 'archiv' directory if it doesn't exist
                archiv_path = os.path.join(directory, 'archiv')
                if not os.path.exists(archiv_path):
                    os.makedirs(archiv_path)

                # Check if file already exists in 'archiv' directory
                archive_path = os.path.join(archiv_path, filename)
                if os.path.exists(archive_path):
                    # Add as many numbers to the filename as needed to make it unique
                    base_archive, ext_archive = os.path.splitext(archive_path)
                    i = 1
                    while os.path.exists(archive_path):
                        archive_path = f"{base_archive}_{i}{ext_archive}"
                        i += 1

                # Move the existing file to the 'archiv' directory
                shutil.move(os.path.join(directory, filename), archive_path)


        if filetype is None:
            filetype = ext[1:]

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

    def get_string_seperator(self) -> str:
        '''Returns the string seperator'''
        return self.string_seperator
