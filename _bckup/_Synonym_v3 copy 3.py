# 6 aug, Saturday, 15:33

#инструкция 
#  $ в ячейке - значит слово всегда оставляется как есть
# %слово% - выделить нужное слово для склонения, если их несколько 

#попробовать объект morph переместить наверх 


import pymorphy2
from pandas import *
import random
import sys


def main():
    inputFileName = 'files/a1.csv'   # сделать input
    outputFileName = inputFileName.replace('.csv', '') + '_result.txt'
    words, formulas = Reader(inputFileName)
    print(f'Максимум вариантов: {Checker(words, formulas):,}')
    max = int(input('Сколько вариантов сделать? '))
    i = 0
    errorCount = 0
    f = open(outputFileName, 'w')
    morph = pymorphy2.MorphAnalyzer()
    while i < max:
        phrase = Generator(words, formulas)
        phrase = Inflector(phrase, morph)
        if phrase:
            phrase = formatPhrase(phrase)
            f.write(phrase + '\n')
            i += 1
        else:
            errorCount += 1
    f.close()
    print(f'Done: {max}. Errors: {errorCount}')



def Reader(file_name):

    # READING
    
    csvData = read_csv(file_name, keep_default_na=False)
    final_list = []
    formulas = []
    for colNum, colName in enumerate(csvData):
        if colNum == 0:
            for formula in csvData[colName].tolist():  # formulas (column A)
                formulas.append(formula)
        elif not 'Unnamed' in colName:  # если столбец со словами (в названии id)
            final_list.append([])
            for word in csvData[colName].tolist():
                final_list[-1].append({})
                final_list[-1][-1]['word'] = word

                try:
                    id, parent_id = colName.split(':')
                except ValueError:
                    id = colName
                    parent_id = None    # тут изменил '' на None 
                final_list[-1][-1]['id'], final_list[-1][-1]['parent_id'] = id, parent_id
        else:   # если столбец таблицы с доп информацией (название пустое)
            for row, effect in enumerate(csvData[colName].tolist()):
                final_list[-1][row]['effect'] = effect


    # CLEANING

    removeList = []
    for formula in formulas:
        if formula == '':
            removeList.append(formula)
    for formula in removeList:
        formulas.remove(formula)

    removeList = []
    for n, list in enumerate(final_list):
        for word in list:
            if word['word'] == '':
                removeList.append({})
                removeList[-1]['n'], removeList[-1]['item'] = n, word
    for list in removeList:
        final_list[list['n']].remove(list['item'])

    for n, formula in enumerate(formulas):
        formulas[n] = formula.replace(' ', '').split('+')

    return final_list, formulas

def Generator(listOfListsOfWords, formulas):
    phrase = []
    formula = random.choice(formulas)
    for letter in formula:
        for list in listOfListsOfWords:
            if list[0]['id'] == letter:
                workingList = listOfListsOfWords.index(list)
                break
        phrase.append(random.choice(listOfListsOfWords[workingList]))
    return phrase 

def Inflector(phrase, morph):


    try:
        rightPhrase = ''
        for word in phrase:
            if word['parent_id'] != None and word['word'].count('$') == 0:
                inflectEffects = set()
                for donorWord in phrase:
                    if donorWord['id'] in word['parent_id']:
                        try:
                            donorWord['effect'] = donorWord['effect'].strip()
                            for effect in donorWord['effect'].split(' '):
                                inflectEffects.add(effect)
                        except KeyError:
                            print(f'Missing effect on parent-word: {donorWord}, \n for word: {word}.')
                            sys.exit()


                wordToInflect = word['word']
                if '%' in word['word']:
                    rIndex = 0
                    while True:
                        try:
                            lIndex = wordToInflect.index('%', rIndex)
                            rIndex = wordToInflect.index('%', lIndex+1)
                            wordToInflect = wordToInflect[lIndex+1:rIndex]
                            inflectResult = morph.parse(wordToInflect)[0]
                            for effect in inflectEffects:
                                iterationEffect = set()
                                iterationEffect.add(effect)
                                inflectResult = inflectResult.inflect(iterationEffect)
                            word['word'] = word['word'].replace(wordToInflect, inflectResult.word)
                            rIndex += 1
                        except ValueError:
                            break
                else:
                    inflectResult = morph.parse(wordToInflect)[0]
                    for effect in inflectEffects:
                        iterationEffect = set()
                        iterationEffect.add(effect)
                        inflectResult = inflectResult.inflect(iterationEffect)
                    word['word'] = inflectResult.word
            if rightPhrase != '':
                rightPhrase += ' '
            rightPhrase += word['word']
        return rightPhrase
    except (AttributeError, TypeError) as e:
        with open('notInflected.txt', 'a') as f:
            f.write(str(phrase) + '\n')
            f.write(str(e) + '\n')
            f.write('\n')


def formatPhrase(string):
    string = string.replace(' ?', '?')
    string = string.replace(' !', '!')
    string = string.replace(' .', '.')
    string = string.replace(' :', ':')
    string = string.replace(' ,', ',')
    string = string.replace('%', '')
    string = string.replace('$', '')
    string = string.strip()
    string = string.replace('  ', ' ')
    string = string.capitalize()
    startOfSentence = string.find('.', 0, -2) + 2
    if startOfSentence != 1:
        string = string[0:startOfSentence] + string[startOfSentence].upper() + string[startOfSentence+1:]
    startOfSentence = string.find('!', 0, -2) + 2
    if startOfSentence != 1:
        string = string[0:startOfSentence] + string[startOfSentence].upper() + string[startOfSentence+1:]
    startOfSentence = string.find('😊', 0, -2) + 2
    if startOfSentence != 1:
        string = string[0:startOfSentence] + string[startOfSentence].upper() + string[startOfSentence+1:]
    startOfSentence = string.find('?', 0, -2) + 2
    if startOfSentence != 1:
        string = string[0:startOfSentence] + string[startOfSentence].upper() + string[startOfSentence+1:]
    startOfSentence = string.find('?)', 0, -2) + 3
    if startOfSentence != 2:
        string = string[0:startOfSentence] + string[startOfSentence].upper() + string[startOfSentence+1:]
    return string
    

def Checker(listOfListsOfWords, formulas):

    final_sum = 0

    for formula in formulas:
        sum = 1
        for letter in formula:
            for list in listOfListsOfWords:
                if list[0]['id'] == letter:
                    workingList = listOfListsOfWords.index(list)
                    break
            sum = sum * len(listOfListsOfWords[workingList])
        final_sum += sum
    
    return final_sum

main()