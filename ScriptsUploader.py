# Программа для массовой загрузки скриптов в сервис Soc Sender


import requests
from bs4 import BeautifulSoup
import datetime
import subprocess

file_names = {
    'files/b3 fix_result_pt1_socsender.txt': 'https://soc-sender.ru/templates?category=70768&project=3348',
    'files/b3 fix_result_pt2_socsender.txt': 'https://soc-sender.ru/templates?category=70988&project=3349',
    'files/b3 fix_result_pt3_socsender.txt': 'https://soc-sender.ru/templates?category=74454&project=3567',
    'files/b3 fix_result_pt4_socsender.txt': 'https://soc-sender.ru/templates?category=74454&project=3567'
}

login_data = {
    'LoginForm[email]': 'spiritcoaching.technical@gmail.com',
    'LoginForm[password]': 'SKAldja0IOJAlksda0ASkdja0123',
    'yt0': 'Войти'
}


deleteJsonUrl = 'https://soc-sender.ru/templates/deleteJson'
saveJsonUrl = 'https://soc-sender.ru/templates/saveJson'

s = requests.Session()
loginURL = 'https://soc-sender.ru/users/login'
r = s.get(loginURL)
soup = BeautifulSoup(r.content, 'html5lib')
login_data['YII_CSRF_TOKEN'] = soup.find('input', attrs = {'name': "YII_CSRF_TOKEN"})['value']
r = s.post(loginURL, data=login_data)

token = login_data['YII_CSRF_TOKEN']

for file_name in file_names:

    #targetTemplatesPageURL = input(f'Target url to {file_name}: ')
    targetTemplatesPageURL = file_names[file_name]

    categoryId = int(targetTemplatesPageURL[targetTemplatesPageURL.find('category=') + 9:targetTemplatesPageURL.find('&', targetTemplatesPageURL.find('category=') + 9)])
    projectId = int(targetTemplatesPageURL[targetTemplatesPageURL.find('project=')+8:])

    # DELETING

    form_data = {
        'YII_CSRF_TOKEN':token
    }


    r = s.get(targetTemplatesPageURL)
    soup = BeautifulSoup(r.content, 'html5lib')
    print('deleting..')
    for hit in soup.findAll(attrs={'class' : 'delete-table-button'}):
        form_data['id'] = hit['data-id']
        r = s.post(deleteJsonUrl, data = form_data)
        print(r.json)


    # COPYING

    form_data = {
        'YII_CSRF_TOKEN':token,
        'id':0,
        'categoryId':categoryId,
        'projectId':projectId,
        'isActive':1,
        'gender':0
    }


    print('copying..')

    with open(file_name) as f:
        for line in f.readlines():
            form_data['body'] = line
            r = s.post(saveJsonUrl, data = form_data)
            print(r.json)





print('Done.')
