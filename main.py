'''This is the main file of the EmotionTool. It is the only file you have to run to use the EmotionTool.'''

from functions import exit_programm
from settings import ET_LABELS, OUTPUT_FILE_URL, INPUT_FILE_URL, ENCODING, SEPERATOR, EMOTION_WORDS_URL, NEGATIONS_URL, INTENSIFIER_URL, LABELS_RAISING_PROBLEMS, CODER, LABELS_TO_LOOK_THROUGH, LABELS_TO_SHOW, VALENCE_PAIRS, LOGO, NO_EMOTION_FOUND_LABEL
from io_machine import IOMachine
from et import ET
from emotion_tool import EmotionTool
from user_interface import UserInterface
from et_structure import Wordlist, DataFrame

def main():
    '''Main Function'''


    print("")
    print(LOGO)
    print("")

    ui = UserInterface()
    io = IOMachine(encoding=ENCODING, delimiter=SEPERATOR, ui=ui)

    # check if something was messed up in the settings-file
    if list(ET_LABELS) != ["emotion", "reduction", "intensifier", "negation", "problems", "coder"]:
        ui.display_message("Hey, you changed something in the settings-file variable 'ET_LABELS', didn't you? The keys of the dictionary have to stay the same. Please fix that.")
        exit_programm()

    # loading wordlist
    wordlist = Wordlist(io=io, emotions_dict_url=EMOTION_WORDS_URL, intensifier_dict_url=INTENSIFIER_URL, negations_dict_url=NEGATIONS_URL)

    # creating ET
    et = ET(wordlist=wordlist, answer_columns=LABELS_TO_LOOK_THROUGH, labels_raising_problem=LABELS_RAISING_PROBLEMS)

    # Creating the DataFrame instance. It automatically loads the input file and converts it into a list of EmotionLines
    df = DataFrame(input_file_url=INPUT_FILE_URL, output_file_url=OUTPUT_FILE_URL, io=io, labels_to_look_through=LABELS_TO_LOOK_THROUGH, et_labels=ET_LABELS)

    # creating EmotionTool instance
    emotion_tool = EmotionTool(ui=ui, df=df, et=et,coder=CODER, labels_to_show=LABELS_TO_SHOW, valence_pairs=VALENCE_PAIRS, no_emotion_found_label=NO_EMOTION_FOUND_LABEL)

    # asking the user, if they want to label the list whole list at once or line by line
    checker = ""
    decision_map = {"0": True, "1": False}
    while checker not in decision_map:
        ui.display_message("You have to Options:\n[0] ET can label the list completely for you\n[1] or you go through every line, where isn't a emotion word yet and you can label it by yourself. ET is still helping you with labeling")
        checker = ui.get_input("What do you want to do?")

    automatic_labeling_decision = decision_map.get(checker, False)

    # labeling the list
    emotion_tool.check_df(automatic_labeling_decision)

    # good bye message
    ui.display_message("Thanks for using the EmotionTool")

if __name__ == "__main__":
    main()
