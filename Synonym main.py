# инструкция 
# программа выдает рандомные фразы из заданных слов-синонимов по заданным шаблонам (формулам) и ставит их в заданные морфологические формы по заданным зависимостям в каждом конкретном предложении.
# нужна CSV таблица
# передать путь к ней в коде в main() в inputFileName 
# в общем нужно передать программе: 1) формулы 2) слова 3) зависимости одних списков слов от других 4) эффекты, которые оказывают конкретные слова
# пример таблицы: https://docs.google.com/spreadsheets/d/1Q0W7kGKGBZzQFkRkcjqrDsUTrhMKQF6a8_a8tDX_vdw/edit?usp=sharing
#
# синтаксис таблицы:
# первая строка - заголовки столбцов (пример: A, B, C. Или: A0, A1, B0, B1). Заголовки должны быть уникальными и не должны входить друг в друга. Плохой пример: A, A1. Правильно: A0, A1
# первый столбец - формулы. Заголовок 1 столбца может быть любым
# пример формулы: A + B + C - склеивает рандомные слова из списков A, B, C 
# синтаксис заголовков стобцов, если нужно склонять слова этого столбца в зависимости от других выбранных слов: A:B C . Расшифровка: столбец называется A, слова в нем берут словоформу из столбцов B и C
# Столбец может ссылаться сам на себя: A:A 
#
# Если слова оказывают влияние, ставить в соседнюю справа колонку их эффекты. Заголовок столбца с эффектами обязательно должен быть пустым!
# игнорировать ячейку при склонении: поставить символ $ в ячейке
# %слово% выделить слово для склонения, можно несколько. Актуально, если в ячейку засовываете словосочетание. Например: %красивый% %слон%

import sys
import random
import re

import pymorphy2
from pandas import *



def main():
    inputFileName = 'files/' + input('Название csv файла (без расширения): ') + '.csv'
    outputFileName = inputFileName.replace('.csv', '') + '_result.txt'
    words, formulas = Reader(inputFileName)
    print(f'Максимум вариантов: {Checker(words, formulas):,}')
    try:
        howMany = int(input('Сколько вариантов сделать? '))
        #howMany = 24000
    except ValueError:
        sys.exit('Это не число')
    i = 0
    errorCount = 0
    f = open(outputFileName, 'w')
    morph = pymorphy2.MorphAnalyzer()
    while i < howMany:
        phrase = Generator(words, formulas)
        phrase = Inflector(phrase, morph)
        if phrase:
            phrase = formatPhrase(phrase)
            f.write(phrase + '\n')
            i += 1
        else:
            errorCount += 1
    f.close()
    print(f'Done: {howMany}. Errors: {errorCount}')



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
    try:
        phrase = []
        formula = random.choice(formulas)
        for letter in formula:
            for list in listOfListsOfWords:
                if list[0]['id'] == letter:
                    workingList = listOfListsOfWords.index(list)
                    break
            phrase.append(random.choice(listOfListsOfWords[workingList]))
        return phrase 
    except UnboundLocalError:
        sys.exit('Не найден лист под буквой ' + letter)

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
                if inflectEffects == {''}:
                    pass
                elif '%' in word['word']:
                    rIndex = 0
                    replaces = []
                    while True:
                        try:
                            lIndex = word['word'].index('%', rIndex)
                            rIndex = word['word'].index('%', lIndex+1)
                            wordToInflect = word['word'][lIndex+1:rIndex]
                            inflectResult = morph.parse(wordToInflect)[morphParsePosition(wordToInflect, morph)]
                            for effect in inflectEffects:
                                if effect == '':
                                    pass
                                else:
                                    iterationEffect = set()
                                    iterationEffect.add(effect)
                                    inflectResult = inflectResult.inflect(iterationEffect)
                            replaces.append({})
                            replaces[-1]['old'] = wordToInflect
                            replaces[-1]['new'] = inflectResult.word
                            rIndex += 1
                        except ValueError:
                            for replaceNum, replace in enumerate(replaces):
                                word['word'] = word['word'].replace(replaces[replaceNum]['old'], replaces[replaceNum]['new'])
                            break
                else:
                    inflectResult = morph.parse(wordToInflect)[morphParsePosition(wordToInflect, morph)]
                    for effect in inflectEffects:
                        if effect == '':
                            pass
                        else:
                            iterationEffect = set()
                            iterationEffect.add(effect)
                            try:
                                inflectResult = inflectResult.inflect(iterationEffect)
                            except ValueError:
                                print(f'Unknown Grammeme, word: {wordToInflect}, effect: {iterationEffect}, \n parsed form: {inflectResult}')
                    word['word'] = inflectResult.word
            if rightPhrase != '':
                rightPhrase += ' '
            rightPhrase += word['word']
        return rightPhrase
    except (AttributeError, TypeError) as e:
        with open('notInflected.txt', 'a') as f:
            f.write(str(phrase) + '\n')
            f.write(str(e) + '\n')
            f.write(word['word'] + '\n')
            f.write('\n')


def formatPhrase(string):
    string = re.sub(' +', ' ', string)
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

def morphParsePosition(word, morph):

    special_dictionary = {
        'йога':1,
        'йог':1,
        'всё':1,
        'то':3
    }


    position = 0
    try:
        if word in special_dictionary:
            position = special_dictionary[word]
            morph.parse(word)[position]
            return position
        else:
            for key in special_dictionary:
                if key in word:
                    position = special_dictionary[key]
                    morph.parse(word)[position]
                    return position
            
            return position
    except IndexError:
        return 0

main()