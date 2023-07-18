import re

def str2list(s: str) -> list:

    # removes whitespace at ends
    s = s.strip()

    # reduces multiple whitespaces to one
    s = re.sub(" +", " ", s)

    # converts string to lower keys
    s = s.lower()

    # splits string into list of words, based on whitespaces
    out = s.split()

    # returns list of words
    return out