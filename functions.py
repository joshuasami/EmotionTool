import csv
import re
import pandas as pd
import json
from collections import Counter


class emoword:
    def __init__(self, emotion, reduction, modifier, negation):
        self.emotion = emotion
        self.reduction = reduction
        self.modifier = modifier
        self.negation = negation

    def printword(self):
        print("Emotion: " + self.emotion + ", Reduction: " + self.reduction + ", Modifier: " + self.modifier + ", Negation: " + self.negation)


class library:
  def __init__(self, words, nonwords, modifiers, negations):
    self.words = words
    self.nonwords = nonwords
    self.modifiers = modifiers
    self.negations = negations

def getText():
    f = open("languages.json", encoding="utf8")
    out = json.load(f)
    f.close()
    return out


def checkForEmotions(lib, line):
    doc = str(line).split(" ")
    out = []
    pattern = re.compile('[\W_]+')
    tmpDoc = [pattern.sub('', token.lower()) for token in doc]
    
    
    counter = 0
    for token in tmpDoc:
        if token in lib.words:
            modifier = ""
            negation = ""
            reduction = ""
            #out.append((token, tmp.replace(" ", "")))
            try:
                countMod = counter
                modLooking = True
                while modLooking:
                    modLooking = False
                    for mods in lib.modifiers:
                        if tmpDoc[countMod-len(mods):countMod] == mods:
                            #modifier = " ".join(mods) + " " + modifier
                            countMod = countMod - len(mods)
                            modLooking = True

                    #if modifier[-1] == " ":
                    #    modifier = modifier[:-1]
                modifier = " ".join(tmpDoc[countMod:counter])


                for negs in lib.negations:
                    if tmpDoc[countMod-len(negs):countMod] == negs:
                        negation += " ".join(tmpDoc[countMod-len(negs):countMod])
                        countMod = countMod-len(negs)
            except IndexError:
                pass

            if negation != "":
                tokenNeg = "nicht " + token
                if tokenNeg in lib.words:
                    reduction = lib.words[tokenNeg]
                    #token = negation + " " + token
            else:
                reduction = lib.words[token]

            if modifier != "":
                token = modifier + " " + token
            
            if negation != "":
                token = negation + " " + token

            out.append(emoword(token, reduction, modifier, negation))


        counter += 1

    return out

def getSingleWordList(file):
    out = []

    with open(file, mode='r', encoding="utf8") as infile:
        reader = csv.reader(infile)
        out = [row[0].split() for row in reader]
        out.sort(key=len, reverse=True)

    out = [[y.lower() for y in i] for i in out]
    return out

def addSingleWordList(file, liste, newWord):
    with open(file, mode='a', newline="", encoding="utf8") as infile:
        writer = csv.writer(infile)

        writer.writerow([newWord])

def getWordList():
    mydict = {}

    with open('lists/words.csv', mode='r', encoding="utf8") as infile:
        reader = csv.reader(infile)
        mydict = {rows[0].lower():rows[1].lower() for rows in reader if rows != ""}

    return mydict

def addWordList(dicti, tup):
    with open('lists/words.csv', mode='a', newline="", encoding="utf8") as infile:
        writer = csv.writer(infile)

        out = [str(tup[0]), str(tup[1])]
        writer.writerow(out)

def counter(liste):
	total2 = []
	for i in liste:
		total2.append(len(i))
	for i in list(set(total2)):
		print(str(i) + ": " + str(total2.count(int(i))))

def createDf(file):
    df = pd.read_csv(file, sep=";", encoding='utf-8-sig')
    # Verständnisfrage;"Frage 1";"Nachfrage 1";"Nachfrage 2";"Nachfrage 3";"Nachfrage 4"

    df['Emotion'] = [""] * len(df)
    df['Reduction'] = [""] * len(df)
    df['Modifikator'] = [""] * len(df)
    df['Negation'] = [""] * len(df)
    df['Kodierer'] = [""] * len(df)
    df['Problem'] = [""] * len(df)

    return df

def checkRows(df, firstIgnore, lib, labels):
    # 0 = Verständnisfrage
    # 1 = no Reduction
    # 2 = over 2
    # 3 = 0
    problems = {}
    check = []
    for ind in df.index:

        if df['Emotion'][ind] != "":
            continue

        counter = 0
        out = []

        for i in range(len(labels)):
            out.append(checkForEmotions(lib, df[labels[i]][ind]))
        for y in out:
            counter += len(y)

        if counter == 1:            
            if firstIgnore:
                if out[0] != []:
                    problems[ind] = [out, 0]
                    continue
            
            for i in out:
                if i != []:
                    df['Emotion'][ind] = i[0].emotion
                    df['Reduction'][ind] = i[0].reduction
                    df['Modifikator'][ind] = i[0].modifier
                    df['Negation'][ind]  = i[0].negation
                    df['Kodierer'][ind]  = "E.T."
                    df['Problem'][ind]  = ""
            if df['Reduction'][ind] == "":
                problems[ind] = [out, 1]
        
        elif counter > 1:
            emos = []
            for z in range(len(out)):
                for i in out[z]:
                    if i != []:
                        emos.append(i.emotion)
                        #for y in out:
                        #    if y != []:
                        #        if i.emotion != y.emotion:
                        #            sameEmo = False
                           
            if len(Counter(emos).values()) == 1:
                for i in out:
                    if i != []:
                        df['Emotion'][ind] = i[0].emotion
                        df['Reduction'][ind] = i[0].reduction
                        df['Modifikator'][ind] = i[0].modifier
                        df['Negation'][ind]  = i[0].negation
                        df['Kodierer'][ind]  = "E.T."
                        df['Problem'][ind]  = ""
            else:
                problems[ind] = [out, 2]
        else:
            problems[ind] = [out, 3]

        check.append(counter)

    for ind in problems:
        df['Problem'][ind] = problems[ind][1]

    

    return problems, df

