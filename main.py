import datetime
import os
from dotenv import load_dotenv
import requests
import time
from bs4 import BeautifulSoup
import telegram

teams = ['ЦСКА', 'Торпедо', 'Химки', 'Локомотив', 'Факел', 'Пари', 'Крылья', 'Урал', 'Сочи', 'Оренбург' ,'Динамо' , 'Ахмат', 'Краснодар', 'Ростов', 'Спартак', 'Зенит']
today = []
fresh = []
live = []


def is_begin(flash):
    if 'flash1.gif' in flash:
        return ('Матч не начался')
    elif 'flash.gif' in flash:
        return ('Матч идёт')
    else:
        return ('Матч окончен!')


def get_today_games(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    games = soup.find_all(bgcolor="#F2F2F2")


    for game in games:
        if ':' in game.a.text:
            one = game.a.text.split(' ')
            if one[0] in teams:
                fresh.append(game.a.text)
                live.append(game.find('img'))


def main():
    load_dotenv()
    url = 'https://football.kulichki.net/'
    get_today_games(url)

    token = os.environ['TELEGRAM_TOKEN']
    chat = os.environ['CHAT_ID']

    bot = telegram.Bot(token=token)
    chat_id = chat

    for game in fresh:
        today.append(game)


    while True:
        try:
            fresh.clear()

            get_today_games(url)

            for num, game in enumerate(fresh):
                print(datetime.datetime.now().time(), fresh[num], '-'*(40-len(fresh[num])), today[num], ' '*(40-len(fresh[num])), is_begin(str(live[num])))
                if fresh[num] != today[num]:
                    print(fresh[num], 'ЕСТЬ ГОООЛ !')
                    today[num] = fresh[num]
                    bot.send_message(chat_id=chat_id, text=fresh[num])

            print('='*120)
            time.sleep(30)
        except requests.exceptions.ConnectionError:
            time.sleep(120)
            continue



if __name__ == '__main__':
    main()
