# Парсит все (чтобы найти заблокированные) аккаунты с сайта Soc Sender


import requests
import time
from bs4 import BeautifulSoup
import csv

print(' --- PARSER --- \n')


login_data = {
    'LoginForm[email]': input('EMAIL: '),
    'LoginForm[password]': input('PASSWORD: '),
    'yt0': 'Войти'
}

s = requests.Session()
url = 'https://soc-sender.ru/users/login'
r = s.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
login_data['YII_CSRF_TOKEN'] = soup.find('input', attrs = {'name': "YII_CSRF_TOKEN"})['value']
r = s.post(url, data=login_data)

ProjectID_in_Sender = input('Project ID in Soc Sender please (main sender: 3348, 3349, test sender: 3483): ')
NumOfAccsPages = input('страниц аккаунтов: ')

file_name = input('file name please: ') + '.csv'
f = open(file_name, 'a')
writer = csv.writer(f)


for page_num in range(1, int(NumOfAccsPages) + 1):
    print('parsing page ' + str(page_num))
    r = s.get('https://soc-sender.ru/accounts?VkAccounts_page=' + str(page_num) + '&project=' + ProjectID_in_Sender)
    soup = BeautifulSoup(r.content, 'html5lib')
    list_ = []
    i = 0
    for hit in soup.findAll(attrs={'class' : 'account-status'}):
        if hit.text.count('Введите логин и пароль') != 1:
            list_.append([])
            list_[i].append(hit.text)
            i += 1
            
    i = 0

    for hit in soup.findAll(attrs={'rel' : 'noreferrer'}):
        list_[i].append(hit['href'])
        i += 1

    i = 0

    for hit in soup.findAll(attrs={'class' : 'account-username'}):
        if i < 10:
            try:
                list_[i].append(hit['value'])
                i += 1
            except (KeyError, IndexError):
                break
        else:
            break

    writer.writerows(list_)

f.close()



print('\n done')
