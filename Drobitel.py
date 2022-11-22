# Упаковывает результат программа Synonym (или to_parts) в пачки скриптов для Soc Sender,
# по формату {скрипт 1|скрипт 2|скрипт 3} с учетом макс. ограничения.

import random
import subprocess


file_names = [
    'files/b3 fix_result_pt1',
    'files/b3 fix_result_pt2',
    'files/b3 fix_result_pt3',
    'files/b3 fix_result_pt4'
]

#file_name = input('file name please: ')
for file_name in file_names:

    f = open(file_name + ".txt", "r")

    f.seek(0)
    _len = len(f.read())
    if (_len // 16484 + 1) % 2 == 0: 
        optimal_len = _len // (_len // 16484 + 1)
    else:
        optimal_len = _len // (_len // 16484 + 2)

    i = 0
    # контроль длины строки

    c = 0
    # подсчет количества скриптов

    f.seek(0)
    _strings = f.readlines()
    #разбить файл исходник на строки

    if _strings[-1] == '\n' or _strings[-1] == '':
        _strings.remove(_strings[-1])

    random.shuffle(_strings)


    f1 = open(file_name + "_socsender.txt", "w")
    for k in _strings:
        k = k.replace('\n', '')
        if k == "":
            print('pass on empty string')
            print('pass on line ' + str(c))
            pass
        if i + len(k) >= optimal_len:
            f1.write('}\n')
            i = 0
        if i == 0:
            f1.write('{')
        if i != 0:
            f1.write('|')
        f1.write(k)
        i += len(k)
        c += 1
    f1.write('}')
    f.close()
    f1.close()



print("done")

#subprocess.call(['open', file_name + ' socsender.txt'])

