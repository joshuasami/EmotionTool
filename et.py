from functions import *
from settings import *

def et(allText, lib):

    df = createDf(file)

    problems, df = checkRows(df, firstIgnore, lib, labels)

    df.to_csv(outFile, index=False, sep=";", encoding='utf-8-sig')

    count_liste = []
    for ind in problems:
        count_liste.append(problems[ind][1])

    print('')
    print(allText['et']['First-Row-Problem'][language] + ":")
    print(count_liste.count(0))
    print('')
    print(allText['et']['No-Reduction-Problem'][language] + ":")
    print(count_liste.count(1))
    print('')
    print(allText['et']['Over-One-Problem'][language] + ":")
    print(count_liste.count(2))
    print('')
    print(allText['et']['Nothing-Found-Problem'][language] + ":")
    print(count_liste.count(3))
    print('')
    print(allText['general-phrases']['total'][language] + ":")
    print(len(problems))

    return problems, df
