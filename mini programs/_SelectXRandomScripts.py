import random

file_name = input('file name please: ')

scriptsNumber = int(input('number of random scripts: '))

new_file_name = file_name + '_' + str(scriptsNumber) + '_random.txt'
file_name = file_name + '.txt'


f = open(file_name, 'r')
f1 = open(new_file_name, 'w')
lines = f.readlines()
for i in range(scriptsNumber):
    f1.write(random.choice(lines))
f.close()
f1.close()
    
print('done')
print('file: ' + new_file_name)
