import csv
import re
import json
from collections import Counter
from settings import *

def exit_programm() -> None:
    print("The programm will close itself done now...") 
    exit()

def getSingleWordList(file):
    out = []

    with open(file, mode='r', encoding="utf8") as infile:
        reader = csv.reader(infile, delimiter=seperator)
        out = [row[0].split() for row in reader]
        out.sort(key=len, reverse=True)

    out = [[y for y in i] for i in out]
    return out

def addSingleWordList(file, liste, newWord):
    with open(file, mode='a', newline="", encoding="utf8") as infile:
        writer = csv.writer(infile, delimiter=seperator)

        writer.writerow([newWord])

def getWordList():
    mydict = {}

    with open('lists/words.csv', mode='r', encoding="utf8") as infile:
        reader = csv.reader(infile, delimiter=seperator)
        mydict = {row[0]:row[1] for row in reader if len(row) == 2}

    return mydict

def addWordList(dicti, tup):
    with open('lists/words.csv', mode='a', newline="", encoding="utf8") as infile:
        writer = csv.writer(infile, delimiter=seperator)

        out = [str(tup[0]), str(tup[1])]
        writer.writerow(out)



def counter(liste):
	total2 = []
	for i in liste:
		total2.append(len(i))
	for i in list(set(total2)):
		print(str(i) + ": " + str(total2.count(int(i))))


def checker01(allText):
    checker = ""

    while checker not in ["0", "1"]:
        checker = input(allText['ec']['next'][language] + " " + allText['general-phrases']['01choice'][language])

    return checker
