import re

def str2list(s: str) -> list:
    '''This Method is used to clean strings and return them in a list format.'''
    # removes whitespace at ends
    s = s.strip()

    # reduces multiple whitespaces to one
    s = re.sub(" +", " ", s)

    # only keep letter, numbers and spaces
    s = re.sub("[^\w\d\s]","",s)

    s = s.lower()

    # splits string into list of words, based on whitespaces
    out = s.split()

    # returns list of words
    return out