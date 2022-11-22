f = open('c1_1+2.txt', 'r')
strings = f.readlines()

f1 = open('c1_1.txt', 'a')
f2 = open('c1_2.txt', 'a')

i = 1

for line in strings:
    if i%2 == 0:
        f1.write(line)
    else:
        f2.write(line)
    i += 1

f.close()
f1.close()
f2.close()

