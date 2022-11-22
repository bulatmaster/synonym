# перед тем как сделать вывод / обработку по одной фразе 


import pymorphy2
from pandas import *



def main():
    inputFileName = 'a2_test.csv'   # сделать input
    outputFileName = inputFileName.replace('.csv', '') + '_result.txt'
    words, formulas = Reader(inputFileName)
    
    phrases = Generator(words, formulas)
    right_phrases = Inflector(phrases)

    with open(outputFileName, 'w') as f:
        for phrase in right_phrases:
            f.write(phrase + '\n')
        
    print('done')

    #Generator(words, formulas)



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


    return final_list, formulas

def Generator(listOfListsOfWords, formulas):

    #  ListOfListsOfWords имеет такой вид:
    #  [[{...},{...}],[{...},{...}]]
    #  [[{'word':'кошка', 'id':'A', 'parent_id':'B', 'effect':'sing'}, {...}], [{...},{...}]]
    #  список списков, в каждом списке - слова, каждое слово - словарь
    for n, formula in enumerate(formulas):
        formulas[n] = formula.replace(' ', '').split('+')
    #  формулы имеют такой вид:  [['A', 'B', 'C'], ['A0', 'Bpref', 'C']]

    phrases = []

    for formula in formulas: 
        for letterPosition, letter in enumerate(formula):
            for list in listOfListsOfWords:   # определить нужный лист по букве формулы 
                if letter in list[0]['id']:
                    workingList = listOfListsOfWords.index(list)   #workingList = номер нужного листа
                    break

            if letterPosition == 0:  # начать фразу 
                for word in listOfListsOfWords[workingList]:
                    phrases.append([])
                    phrases[-1].append(word) 
            else:                    # продолжить фразу 
                iteration = phrases
                phrases = []
                for word in listOfListsOfWords[workingList]:
                    for not_ready_phrase in iteration:
                        phrases.append(not_ready_phrase.copy())
                        phrases[-1].append(word)

    return phrases


def Inflector(listOfPhrases):

    with open('listOfPhrases', 'w') as f:
        f.write(str(listOfPhrases))


    morph = pymorphy2.MorphAnalyzer()
    rightPhraseList = []
    for phrase in listOfPhrases:
        try:
            rightPhrase = ''
            for word in phrase:
                if word['parent_id'] != None:
                    for donorWord in phrase:
                        if donorWord['id'] == word['parent_id']:
                            inflectResult = morph.parse(word['word'])[0].inflect({donorWord['effect']})
                            word['word'] = word['word'].replace(word['word'], inflectResult.word)
                if rightPhrase != '':
                    rightPhrase += ' '
                rightPhrase += word['word']
            rightPhrase = formatString(rightPhrase)
            rightPhraseList.append(rightPhrase)
        except AttributeError:
            with open('notInflected.txt', 'a') as f:
                f.write(str(phrase))
                f.write('\n\n')

    return rightPhraseList

def formatString(string):
    string = string.replace(' ?', '?')
    string = string.replace(' !', '!')
    string = string.replace(' .', '.')
    string = string.strip()
    string = string.capitalize()
    return string
    

main()