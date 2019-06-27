import getch
wordFile=open("wordFile.txt")
wordList=wordFile.read().split()
phrase=""


while True:
    input=getch.getch()
    choiceList=[]
    try:
        if int(input)==0:
            phrase = phrase[:-1]
    except:
        phrase += input

    print(phrase)
    for i in range(len(wordList)):
        if phrase in (wordList[i]):
            choiceList.append(wordList[i])

    if len(choiceList) >= 10:

        print("There is " + str(10) +" predictions available.\n"
                                         "Press the corresponding number to autocomplete.\n"
                                         "The predictions are as follows:\n"
                                         "\t0. Backspace")
        for i in range(10):
            print("\t" + str(i+1) + ". " + choiceList[i])
            try:
                for i in range(10):
                    if int(input)==i+1:
                        phrase=choiceList[i]
            except:
                pass

    if len(choiceList) < 10:

        print("There is " + str(len(choiceList)) + " predictions available.\n"
                                 "Press the corresponding number to autocomplete.\n"
                                 "The predictions are as follows:\n"
                                 "\t0. Backspace")
        for i in range(len(choiceList)):
            print("\t" + str(i + 1) + ". " + choiceList[i])
            try:
                for i in range(len(choiceList)):
                    if int(input) == i + 1:
                        phrase = choiceList[i]
            except:
                pass