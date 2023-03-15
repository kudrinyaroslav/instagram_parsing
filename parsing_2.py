#!/usr/bin/python3

"""
Описание скрипта

в цикле - скачиваем список пользователей --> генерируем новый after --> парсим в многопоточности --> сохраняем в csv

"""


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
user_id = '14682088361'

def GET_USER_LIST(user_id, headers, after):
    idifier = '{{"id":"{user_id}","include_reel":true,\
            "fetch_mutual":false,"first":50,"after":"{after}"}}'.format(user_id=user_id,after=after)
    params = [
            ['query_hash', 'c76146de99bb02f6415203be841dd25a'],
            ['variables', idifier]]
    response = requests.get('https://www.instagram.com/graphql/query/',
                            headers=headers, params=params
                            )
    data = json.loads(response.text)
    return data

def PARSING_USER(user, SAVER):
    user_info = user['node']
    params = (('__a', '1'),)
    username = user_info['username']
    response = requests.get(url.format(username=username), headers=headers, params=params)
    data_user = json.loads(response.text)
    SAVER(data_user, username)


def SAVE_TO_CSV(data_user, username):
    with open('followers.csv', 'a') as f:
        posts = data_user['graphql']['user']
        posts = posts['edge_owner_to_timeline_media']['count']
        followers = data_user['graphql']
        followers = followers['user']['edge_followed_by']['count']
        f.write(f"""{username},{posts},{followers}\n""")



if __name__ == '__main__':
    while True:
        data = GET_USER_LIST(user_id, headers, after)
        after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
        users = data['data']['user']['edge_followed_by']['edges']
        for user in users:
            PARSING_USER(user, SAVE_TO_CSV)
        index += 1
        if not data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
            break
        
