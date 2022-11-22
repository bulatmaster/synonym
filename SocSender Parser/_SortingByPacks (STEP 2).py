# Сортирует результат предыдущего шаша по пачкам, из которых были аккаунты, и находит пароли к ним.
# Для этого нужны исходники файлов с логинами-паролями.


import csv

file_name = input('file name please: ')
f = open(file_name + '.csv', 'r')
w = open(file_name + ' by groups.csv', 'w')

with open('pack2.txt', 'r') as fp2:
    pack2 = fp2.read()

with open('pack3.txt', 'r') as fp3:
    pack3 = fp3.read()
    fp3.seek(0)
    pack3_lines = fp3.readlines()

frows = csv.reader(f)

i1 = 0
i2 = 0
i3 = 0

writer = csv.writer(w)


for row in frows:
    if pack3.count(row[2]) == 1:
        row.append('пачка 3')
        i3 += 1
        for pack3_line in pack3_lines:
            if pack3_line.count(row[2]) == 1:
                pack3_line = pack3_line.replace('\n', '')
                row.append(pack3_line)
        writer.writerow(row)
        
    elif pack2.count(row[2]) == 1:
        row.append('пачка 2')
        i2 += 1
        writer.writerow(row)
    else:
        row.append('пачка 1')
        i1 += 1
        writer.writerow(row)


writer.writerows(frows)


f.close()
w.close()

print('pack 1: ', str(i1))
print('pack 2: ', str(i2))
print('pack 3: ', str(i3))
print('done')
