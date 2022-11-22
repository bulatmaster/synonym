file_name = input('file name: ')
with open(file_name + '.txt', 'w') as f:
    with open('похоже, у нас общие интересы.txt', 'r') as d:
              content = d.readlines()
              for line in content:
                  f.write(line)
              
    with open('я пишу, потому что , похоже, у нас общие интересы.txt', 'r') as d:
              content = d.readlines()
              for line in content:
                  f.write(line)
