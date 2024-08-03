'''This is the main file of the EmotionTool. It is the only file you have to run to use the EmotionTool.'''

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from settings import ET_LABELS, OUTPUT_FILE_URL, INPUT_FILE_URL, ENCODING, SEPERATOR, EMOTION_WORDS_URL, NEGATIONS_URL, MODIFIER_URL, LABELS_RAISING_PROBLEMS, CODER, LABELS_TO_LOOK_THROUGH, LABELS_TO_SHOW, VALENCE_PAIRS, LOGO, NO_EMOTION_FOUND_LABEL, WORDLIST_LABELS, STRING_SEPERATOR
from modules.io_machine import IOMachine
from modules.et import ET
from modules.emotion_tool import EmotionTool
from modules.user_interface import UserInterface
from modules.et_structure import Wordlist, DataFrame

def main():
    '''Main Function'''

    # creating the UserInterface instance
    ui = UserInterface()

    # creating the IOMachine instance
    io = IOMachine(encoding=ENCODING, delimiter=SEPERATOR, string_seperator=STRING_SEPERATOR, ui=ui)

    # print the logo
    ui.print_empty_line()
    ui.display_message(LOGO)
    ui.print_empty_line()

    # check if something was messed up in the settings-file
    if list(ET_LABELS) != ["emotion", "reduction", "modifier", "negation", "problems", "coder"]:
        ui.display_message("Hey, you changed something in the settings-file variable 'ET_LABELS', didn't you? The keys of the dictionary have to stay the same. Please fix that.")
        sys.exit(0)

    # loading wordlist
    wordlist = Wordlist(io=io, wordlist_labels=WORDLIST_LABELS, emotions_dict_url=EMOTION_WORDS_URL, modifier_dict_url=MODIFIER_URL, negations_dict_url=NEGATIONS_URL)

    # creating ET
    et = ET(wordlist=wordlist, valence_pairs=VALENCE_PAIRS, labels_raising_problem=LABELS_RAISING_PROBLEMS, string_seperator=STRING_SEPERATOR)

    # Creating the DataFrame instance. It automatically loads the input file and converts it into a list of EmotionLines
    df = DataFrame(input_file_url=INPUT_FILE_URL, output_file_url=OUTPUT_FILE_URL, io=io, labels_to_look_through=LABELS_TO_LOOK_THROUGH, et_labels=ET_LABELS)

    # creating EmotionTool instance
    emotion_tool = EmotionTool(ui=ui, df=df, et=et,coder=CODER, labels_to_show=LABELS_TO_SHOW, valence_pairs=VALENCE_PAIRS, no_emotion_found_label=NO_EMOTION_FOUND_LABEL)

    # labeling the list
    emotion_tool.check_df()

    # good bye message
    ui.display_message("Thanks for using the EmotionTool")


if __name__ == "__main__":
    main()
