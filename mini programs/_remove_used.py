f1 = open('a1.txt', 'r')
f2 = open('a1_6000random.txt', 'r')
f3 = open('a1_without_used.txt', 'w')

all16k = f1.readlines()
all6k = f2.readlines()

for i in all6k:
    try:
        all16k.remove(i)
    except ValueError:
        f3.write(i)

print('done')
