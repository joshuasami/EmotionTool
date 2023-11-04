'''This is the main file of the EmotionTool. It is the only file you have to run to use the EmotionTool.'''

from functions import exit_programm, check_special_letters, check_dicts
from settings import ET_LABELS, INPUT_FILE_URL, EMOTION_WORDS_URL, NEGATIONS_URL, INTENSIFIER_URL, ENCODING, SEPERATOR, OUTPUT_FILE, LABELS_TO_LOOK_THROUGH, LABELS_RAISING_PROBLEMS, CODER, LABELS_TO_SHOW, VALENCE_PAIRS, LOGO
from io_machine import IOMachine
from et_io_conversion import load_emotion_dict, load_single_list, load_df, convert_df, convert_emotion_dict, convert_single_list
from et import ET
from ec import EmotionClicker

def main():
    '''Main Function'''


    print("")
    print(LOGO)
    print("")

    # check if something was messed up in the settings-file
    if list(ET_LABELS) != ["emotion", "reduction", "intensifier", "negation", "problems", "coder"]:
        print("Hey, you changed something in the settings-file variable 'ET_LABELS', didn't you? The keys of the dictionary have to stay the same. Please fix that.")
        exit_programm()

    # creating the IOMachine instance
    io = IOMachine(ENCODING, SEPERATOR)


    # loading wordlist
    try:
        emotion_dict_raw = io.load_file(EMOTION_WORDS_URL)
        if not check_dicts(emotion_dict_raw):
            raise Exception("The table structure isn't homogeneous")
        check_special_letters(emotion_dict_raw, EMOTION_WORDS_URL)
        emotion_dict = load_emotion_dict(emotion_dict_raw, row_1='emotion')
    except Exception as error:
        print("The wordlist couldn't be loaded")
        print(error)
        exit_programm()

    # loading negation-wordlist
    try:
        negations_raw = io.load_file(NEGATIONS_URL)
        if not check_dicts(negations_raw):
            raise Exception("The table structure isn't homogeneous")
        check_special_letters(negations_raw, NEGATIONS_URL)
        negations = load_single_list(negations_raw)
    except Exception as error:
        print("The negations-wordlist couldn't be loaded")
        print(error)
        exit_programm()

    # loading intensifier-wordlist
    try:
        intensifiers_raw = io.load_file(INTENSIFIER_URL)
        if not check_dicts(intensifiers_raw):
            raise Exception("The table structure isn't homogeneous")
        check_special_letters(intensifiers_raw, INTENSIFIER_URL)
        intensifiers = load_single_list(intensifiers_raw)
    except Exception as error:
        print("The intensifier-wordlist couldn't be loaded")
        print(error)
        exit_programm()

    # creating ET
    et = ET(emotion_dict = emotion_dict, intensifiers = intensifiers, negations = negations, labels_raising_problem=LABELS_RAISING_PROBLEMS)

    # loading input-file
    try:
        header_row = io.get_csv_header(INPUT_FILE_URL)
        input_file_raw= io.load_file(INPUT_FILE_URL)
        if not check_dicts(input_file_raw):
            raise Exception("The table structure isn't homogeneous")
        check_special_letters(input_file_raw, INPUT_FILE_URL)
        df = load_df(input_list=input_file_raw, labels_to_look_through=LABELS_TO_LOOK_THROUGH, et_labels=ET_LABELS)
    except Exception as error:
        print("The input-file couldn't be loaded")
        print(error)
        exit_programm()


    print("")



    # creating EmotionClicker instance
    ec = EmotionClicker(df=df, et=et,coder=CODER, labels_to_show=LABELS_TO_SHOW, valence_pairs=VALENCE_PAIRS)


    # asking the user, if they want to label the list whole list at once or line by line
    checker = ""
    decision_map = {"0": True, "1": False}
    while checker not in decision_map:
        print("You have to Options:\n[0] ET can label the list completely for you\n[1] or you go through every line, where isn't a emotion word yet and you can label it by yourself. ET is still helping you with labeling")
        checker = input("What do you want to do?")

    
    automatic_labeling_decision = decision_map.get(checker, False)

    # labeling the list
    ec.check_df(automatic_labeling_decision)

    # converting the df back to a list of dictionaries, so it can be saved
    df_raw = convert_df(df=df,et_labels=ET_LABELS)

    # adding the ET_LABELS to the header_row, if they aren't already in there
    for col in ET_LABELS.values():
        if col not in header_row:
            header_row.append(col)


    # saving the df

    io.save_file(file=OUTPUT_FILE, output_content=df_raw, filetype="csv", header_row=header_row)

    # updating the intensifier-wordlist
    intensifiers_raw = convert_single_list(input_list=ec.et.intensifiers, name="intensifiers")
    io.save_file(file=INTENSIFIER_URL, output_content=intensifiers_raw, filetype="csv")

    # updating the negation-wordlist
    negations_raw = convert_single_list(input_list=ec.et.negations, name="negations")
    io.save_file(file=NEGATIONS_URL, output_content=negations_raw, filetype="csv")

    # updating the emotion-wordlist
    emotion_dict_raw = convert_emotion_dict(input_dict=ec.et.emotion_dict, row_1='emotion')
    io.save_file(file=EMOTION_WORDS_URL, output_content=emotion_dict_raw, filetype="csv")

    # good bye message
    print("Thanks for using the EmotionTool")

if __name__ == "__main__":
    main()
