import pymorphy2
from pandas import *


def main():
    words = Reader()
    phrases = Generator(words)
    right_phrases = Inflector(phrases)

    for phrase in right_phrases:
        print(phrase)


def Reader():

    # READING
    file_name = 'a2_test.csv'   # здесь будет input или удоьный способ помещать файл 
    csvData = read_csv(file_name, keep_default_na=False)
    final_list = []
    for colNum, colName in enumerate(csvData):
            if not 'Unnamed' in colName:  # если столбец со словами (в названии индекс)
                final_list.append([])
                for word in csvData[colName].tolist():
                    final_list[-1].append({})
                    final_list[-1][-1]['word'] = word
                    try:
                        id, parent_id = colName.split(':')
                    except ValueError:
                        id = colName
                        parent_id = ''
                    final_list[-1][-1]['id'], final_list[-1][-1]['parent_id'] = id, parent_id
            else:   # если столбец таблицы с доп информацией (название пустое)
                for row, effect in enumerate(csvData[colName].tolist()):
                    final_list[-1][row]['effect'] = effect


    # CLEANING
    removeList = []
    for n, list in enumerate(final_list):
        for word in list:
            if word['word'] == '':
                removeList.append({})
                removeList[-1]['n'], removeList[-1]['item'] = n, word
    for list in removeList:
        final_list[list['n']].remove(list['item'])


    return final_list

def Generator(inputData):

    phraseList = []

    for word in inputData[0]:
        phraseList.append([])
        phraseList[-1].append(word)

    for list in inputData[1:]:
        iteration = phraseList
        phraseList = []
        for word in list:
            for not_ready_phrase in iteration:
                phraseList.append(not_ready_phrase.copy())
                phraseList[-1].append(word)

    return phraseList


def Inflector(listOfPhrases):

    morph = pymorphy2.MorphAnalyzer()
    rightPhraseList = []
    for phrase in listOfPhrases:
        rightPhrase = ''
        for word in phrase:
            if word['parent_id'] != None:
                for item_iter2 in phrase:
                    findResult = word['parent_id'].find(item_iter2['id'])
                    inflect_effect = ''
                    if -1 < findResult < leastFindResult:
                        leastFindResult = findResult
                        inflect_effect = item_iter2['effect']
                word['word'] = morph.parse(word['word'])[0].inflect({inflect_effect}).word
            if rightPhrase != '':
                rightPhrase += ' '
            rightPhrase += word['word']
        rightPhrase = rightPhrase.capitalize().replace(' ?', '?')
        rightPhraseList.append(rightPhrase)

    return rightPhraseList

main()