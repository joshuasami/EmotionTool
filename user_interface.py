'''This module contains the UserInterface class'''

class UserInterface:
    '''A class that handles any interaction with the user'''

    def __init__(self):
        pass

    def display_message(self, message):
        '''Displays a message to the user'''
        print(message)

    def print_empty_line(self, n: int = 1):
        '''Prints an empty line'''
        print("\n" * n)

    def get_input(self,prompt):
        '''Asks the user for input and returns it'''
        return input(prompt)
    
    def dict_dict_as_table(self, input_dict: dict[str]) -> str:
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

        self.display_message(out_string)