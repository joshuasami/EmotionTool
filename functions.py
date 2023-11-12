'''This module contains random functions, which are used in the main programm.'''
import sys
import re
from user_interface import UserInterface

def exit_programm() -> None:
    """Exits the programm with exit-code 0"""
    
    print("The programm will close itself done now...") 
    sys.exit(0)

def check_dicts(list_of_dicts):
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

def check_special_letters(raw_file: dict, raw_file_name: str) -> bool:
    """Checks if the raw-file contains special letters, which are than displayed, so the user can check if their were laoded correctly."""

    pattern = re.compile(r"[^A-Za-z0-9\s_\-,#.:]")  # Regex-Muster für nicht erlaubte Zeichen


    for line in raw_file:
        found_special_letter = False
        for value in line.values():
            
            # Prüfen, ob der Satz nicht erlaubte Zeichen enthält
            if re.search(pattern, value):
                found_special_letter = True

        if found_special_letter:
            print(f"Example for {raw_file_name}:\n")
            out_string = dict_to_table(line)
                
            print(out_string)
            print("\n")
            print("\n")
            return True

    return False
            
def dict_to_table(input_dict: dict[str]) -> str:
    """Converts a dictionary to a table, which is returned as a string."""

    max_key_length = max(map(len, input_dict.keys()))
    max_value_length = max(map(len, input_dict.values()))

    max_col_length = max(max_key_length, max_value_length)

    max_col_length += 2

    out_string1 = ""
    out_string2 = ""

    for key, value in input_dict.items():

        if len(out_string2) > 100:
            out_string1 += "|\n"
            out_string2 += "|"
            out_string1 += f"{out_string2}\n\n"
            out_string2 = ""

        max_col_length = max(len(key), len(value))
        max_col_length += 0
        out_string1 += f"|{key: ^{max_col_length}}"
        out_string2 += f"|{value: ^{max_col_length}}"

    out_string1 += "|\n"
    out_string2 += "|"
    
    out_string = out_string1 + out_string2

    return out_string