import random
f = open("cosmo c1.txt", "r")

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


f1 = open("cosmo c1 socsender.txt", "w")
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
f1.write("\n" + str(c) + ' скриптов')
f.close()
f1.close()

print("done")
