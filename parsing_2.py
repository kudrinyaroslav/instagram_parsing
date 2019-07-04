#!/usr/bin/python3


import json
import requests
from time import sleep


# копируем с сайта headers
headers = {
    'cookie': 'mid=XItQQAALAAExEB_83VaDzCS5C-hP;\
    csrftoken=6rI8hSNDrPtfAsB5yMFBCMoPAnbJb93P;\
    ds_user_id=15297523511; sessionid=15297523511%3AcR4hwaesmjUPgP%3A6;\
    rur=PRN; urlgen="{\\"93.187.189.66\\": 48223}:\
    1hhrzM:VYmJUplqM8__weNAFGKPvz_OcZI"',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36""",
    'accept': '*/*',
    'referer': 'https://www.instagram.com/olgaan/followers/',
    'authority': 'www.instagram.com',
    'x-requested-with': 'XMLHttpRequest',
    'x-ig-app-id': '936619743392459',
}

# инициализируем параметр after
# указывает на список следующих
# пользователей - первый after пустой
after = ''
# URL к followers
url = """https://www.instagram.com/{username}/"""
# считаем подписчиков что бы
# делать перерывы между запросами
index = 0

# пишем заголовок в файл
with open('followers.csv', 'w') as f:
    f.write("username, posts, followers\n")

while True:
    # подставляем параметры
    # в запрос с новым after
    idifier = '{{"id":"15361983429","include_reel":true,\
            "fetch_mutual":false,"first":13,"after":"{}"}}'.format(after)
    # подставляем в params новое значение idifier
    params = [
            ['query_hash', 'c76146de99bb02f6415203be841dd25a'],
            ['variables', idifier]]
    # формируем запрос на получение
    # списка пользователей
    response = requests.get('https://www.instagram.com/graphql/query/',
                            headers=headers, params=params
                            )
    # загружаем список в формате json
    data = json.loads(response.text)
    print(data)
    # получаем новое значение after
    after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
    # парсим пользователей из data
    for user in data['data']['user']['edge_followed_by']['edges']:
        user_info = user['node']
        print('while')
        params = (('__a', '1'),)
        username = user_info['username']
        # отправляем запрос на страницу со списком пользователей
        response = requests.get(url.format(username=username),
                                headers=headers, params=params
                                )

        # пытаемся сформировать json data
        try:
            data_user = json.loads(response.text)
        except Exception:
            # если не получилось, ждем 30 секунд
            sleep(30)
            # пробуем еще раз отправить запрос
            # на страницу со списком пользователей
            response = requests.get(url.format(username=username),
                                    headers=headers, params=params
                                    )
            # загружаем список в формат json
            data_user = json.loads(response.text)
        # сохраняем пользователя в файл
        with open('followers.csv', 'a') as f:
            posts = data_user['graphql']['user']
            posts = posts['edge_owner_to_timeline_media']['count']
            followers = data_user['graphql']
            followers = followers['user']['edge_followed_by']['count']
            f.write(f"""{username},{posts},{followers}\n""")
        # засыпаем что бы не заблокировали
        sleep(1 if index % 100 != 0 else 5)
        # прибавляем index
        index += 1
    # проверяем есть ли следующая страница
    # со списком пользователей, если нет,
    # заканчиваем работу скрипта
    data = data['data']['user']
    if not data['edge_followed_by']['page_info']['has_next_page']:
        break
