# программа удаляет из файла со скриптами, которые идут в столбик,
# после программы sinonim, все строки которые содержат введенную фразу

i = 0 # счетчик оставлений
x = 0 # счетчик удалений

file_name = input('file name please: ')

f = open(file_name + ".txt", "r")
_strings = f.readlines()
f.close()
f = open(file_name + "_ScriptsRemoved.txt", "w")

WordForRemove = input('word for remove: ')

for _line in _strings:
    if _line.count(WordForRemove) == 0: #здесь искать слово для удаления
        f.write(_line)
        i += 1
    else:
        x += 1
        
f.close()

print("количество удалений = " + str(x))
print("количество скриптов = " + str(i))
print('done')
