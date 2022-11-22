# программа для ручного создания скриптов
# Как Synonym, только без падежей и надо вручную вводить каждый список слов.
# Используйте, если надо произвести простую операцию или основная программа тупит с падежами.
# Модуль bckup не работает

import sys
import subprocess
sp = ' '

def bckup(file_name):
    try:
        with open(file_name + '.txt') as f_bckup:
            content_bckup = f_bckup.read()
            with open('bckup/' + file_name + ' (bckup).txt', 'w') as f2_bckup:
                f2_bckup.write(content_bckup)
    except FileNotFoundError:
        print('bckup pass')
        pass
    
    



final_list = []
list_num = 1
i = 0  #счетчик созданий
while True:
    print('input list ' + str(list_num) + ' or ctrl+D" ')
    lines = sys.stdin.read().splitlines()
    if lines == []:
        break
    final_list.append(lines)
    list_num += 1



if len(final_list) < 1:
    print('1 or more lists of words please')
elif len(final_list) > 8:
    print('less than 9 lists of words please')
else:
    file_name = 'files/' + input('file name please: ') + '.txt'
    mode = input('opening mode (a/w): ')
    f = open(file_name, mode)
    bckup(file_name)

    if len(final_list) == 1:
        for i0 in final_list[0]:
            phrase = i0 + '\n'
            f.write(phrase)
            i += 1

    if len(final_list) == 2:
        for i0 in final_list[0]:
            for i1 in final_list[1]:
                phrase = i0 + sp + i1 + '\n'
                f.write(phrase)
                i += 1

    elif len(final_list) == 3:
        for i0 in final_list[0]:
            for i1 in final_list[1]:
                for i2 in final_list[2]:
                    if i0 != i2:
                        phrase = i0 + sp + i1 + sp + i2 + '\n'
                        f.write(phrase)
                        i += 1

    elif len(final_list) == 4:
        for i0 in final_list[0]:

            for i1 in final_list[1]:
                for i2 in final_list[2]:
                    for i3 in final_list[3]:
                        phrase = i0 + sp + i1 + sp + i2 + sp + i3 + '\n'
                        f.write(phrase)
                        i += 1

    elif len(final_list) == 5:
        for i0 in final_list[0]:
            for i1 in final_list[1]:
                for i2 in final_list[2]:
                    for i3 in final_list[3]:
                        for i4 in final_list[4]:
                            phrase = i0 + sp + i1 + sp + i2 + sp + i3 + sp + i4 + '\n'
                            f.write(phrase)
                            i += 1

    elif len(final_list) == 6:
        for i0 in final_list[0]:
            for i1 in final_list[1]:
                for i2 in final_list[2]:
                    for i3 in final_list[3]:
                        for i4 in final_list[4]:
                            for i5 in final_list[5]:
                                phrase = i0 + sp + i1 + sp + i2 + sp + i3 + sp + i4 + sp + i5 + '\n'
                                f.write(phrase)
                                i += 1

    elif len(final_list) == 7:
        for i0 in final_list[0]:
            for i1 in final_list[1]:
                for i2 in final_list[2]:
                    for i3 in final_list[3]:
                        for i4 in final_list[4]:
                            for i5 in final_list[5]:
                                for i6 in final_list[6]:
                                    phrase = i0 + sp + i1 + sp + i2 + sp + i3 + sp + i4 + sp + i5 + sp + i6 + '\n'
                                    f.write(phrase)
                                    i += 1

    elif len(final_list) == 8:
        for i0 in final_list[0]:
            for i1 in final_list[1]:
                for i2 in final_list[2]:
                    for i3 in final_list[3]:
                        for i4 in final_list[4]:
                            for i5 in final_list[5]:
                                for i6 in final_list[6]:
                                    for i7 in final_list[7]:
                                        phrase = i0 + sp + i1 + sp + i2 + sp + i3 + sp + i4 + sp + i5 + sp + i6 + sp + i7 + '\n'
                                        f.write(phrase)
                                        i += 1
        f.close()

    f = open(file_name, 'r')
k = 0  # счетчик сколько всего скриптов в файле
lines = f.readlines()
f.close()
def clean():
    f = open(file_name, 'w')
    for line in lines:
        k += 1
        line = line.replace(' ?', '?')
        line = line.replace(' !', '!')
        line = line.replace(' )', ')')
        line = line.replace(' ,', ',')
        line = line.replace(' :', ':')
        line = line.replace(' .', '.')    
        if line[0] == ' ':
            line = line.replace(' ', '', 1)

        f.write(line.capitalize())
    f.close()


print("добавлено " + str(i) + " скриптов.")
print("вcего в файле \""+ file_name + "\" " + str(k) + " скриптов.")
subprocess.call(['open', file_name])

