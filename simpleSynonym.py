lists = [
    [
        'A0 + B + C + D',
        'A1 + B + Cpref + C + D'
    ],
    [
        'E0 + G + H + J',
        'E0 + F + G + H + J',
        'E1 + G + H + J',
        'E0 + Gpref + G + H + J',
        'E0 + F + Gpref + G + H + J',
        'E1 + Gpref + G + H + J',
        'E2 + H + J'
]]

result = []
for i0 in lists[0]:
    for i1 in lists[1]:
        result.append(i0 + ' + ' + i1)
        result.append(i1 + ' + D + ' + i0)

for item in result:
    print(item)
