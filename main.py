import datetime

import requests
import time
from bs4 import BeautifulSoup
import telegram

teams = ['ЦСКА', 'Ливерпуль', 'Брентфорд', 'Эльче']
today = []
fresh = []

def get_today_games():

    url = 'https://football.kulichki.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    games = soup.find_all(bgcolor="#F2F2F2")
    for game in games:
        if ':' in game.a.text:
            one = game.a.text.split(' - ')
            if one[0] in teams:
                fresh.append(game.a.text)



def main():
    bot = telegram.Bot(token='5578510907:AAFBQsQJ9MDEzfrkbDBFZ_lBNtji1gfJvuM')
    chat_id = ('@photos_from_NASA')
    get_today_games()

    for game in fresh:
        today.append(game)

    # print(today)
    # print(fresh)

    while True:

        fresh.clear()
        # print(f'Предыдущий список результатов: {today}')
        # print(f'Обновленный список результатов: {fresh}')
        get_today_games()

        for num, game in enumerate(fresh):
            print(datetime.datetime.now().time(), fresh[num], '---------', today[num])
            if fresh[num] != today[num]:
                print(fresh[num], 'ЕСТЬ ГОООЛ !')
                today[num] = fresh[num]
                bot.send_message(chat_id=chat_id, text=fresh[num])
        print('===================================')
        time.sleep(30)



if __name__ == '__main__':
    main()

# flash.gif - матч идет
# flash2.gif - матч окончен
# flash1.gif - матч не начался