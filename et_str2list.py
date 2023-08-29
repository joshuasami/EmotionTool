import re

def str2list(s: str) -> list:
    '''This Method is used to clean strings and return them in a list format.'''
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