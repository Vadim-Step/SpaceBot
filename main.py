import vk_api
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import database
from functions import func_showing_place, func_play_cities, func_geocoder, func_guess_city, func_distance


def main():
    vk_session = vk_api.VkApi(
        token='3de9c0ce56bb265632da8c7348a37fe081ebd68d9744120f9da0108b82654974ccd938d58ceee8cc26b9c')
    longpoll = VkBotLongPoll(vk_session, '203395569')
    city = None
    asked = False
    lens = False
    asked1 = False
    greet = False
    asked_type = False
    started = False
    renew = False
    score = 0
    city_last = False
    in_menu = True
    city_rand2 = False
    asked2 = False
    first_place = False
    guessing_city = False
    showing_place = False
    played_cities = False
    playing_cities = False
    geocoding = False
    for event in longpoll.listen():
        vk = vk_session.get_api()
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not greet:
                response = vk.users.get(user_id=event.obj.message['from_id'])
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 message=f'Приветствую тебя, {response[0]["first_name"]}')
                greet = True
            if event.message.text.lower() == 'выйти':
                showing_place = False
                playing_cities = False
                geocoding = False
                guessing_city = False
                first_place = False
                score = 0
                in_menu = True
                lens = False
                city = None
                asked = False
                asked2 = False
                asked_type = False
            # навыки:
            if event.message.text == 'Покажи место' or showing_place:
                showing_place, asked, asked_type, city, in_menu = func_showing_place(event, asked,
                                                                                     asked_type, city,
                                                                                     vk, showing_place,
                                                                                     in_menu)
            if (event.message.text == 'zen' or event.message.text == 'пасхалка') and in_menu:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=random.choice(['У самурая нет цели, только путь...',
                                                        'почему так...',
                                                        'не теряем время, нужно решать задачи...']),
                                 keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))

            if event.message.text == 'Рейтинг':
                data = database.getName()
                rating1 = []
                rating2 = []
                try:
                    for i in data:
                        data2 = database.getData(i[0])
                        for j in range(len(data2)):
                            try:
                                rating1.append(f'{i[1]} - {data2[j][3]}')
                                rating2.append(f'{i[1]} - {len(data2[j][2].split())}')
                            except Exception:
                                pass
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Рейтинг игры в города:',
                                     keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
                    if rating1:
                        for i in rating1:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=i,
                                             keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                             random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Нет данных',
                                         keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Рейтинг "угадай город":',
                                     keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
                    if rating2:
                        for i in rating2:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=i,
                                             keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                             random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Нет данных',
                                         keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                except Exception as a:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=a,
                                     keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))

            if event.message.text == 'Геокодер' or geocoding:
                event, asked1, vk, geocoding, in_menu = func_geocoder(event, asked1, vk, geocoding,
                                                                      in_menu)
            if event.message.text == 'Игра в города' or playing_cities:
                try:
                    event, playing_cities, started, city_last, vk, in_menu, played_cities, score = func_play_cities(
                        event, playing_cities, started, city_last, vk, in_menu, played_cities, score)
                except Exception as err:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                     message=f'Произошла ошибка. Вы находитесь в меню.')
                    showing_place = False
                    playing_cities = False
                    geocoding = False
                    guessing_city = False
                    first_place = False
                    score = 0
                    in_menu = True
                    lens = False
                    city = None
                    asked = False
                    asked2 = False
                    asked_type = False
            if event.message.text == 'Угадай город' or guessing_city:
                event, guessing_city, in_menu, asked2, vk, city_rand2 = func_guess_city(event,
                                                                                        guessing_city,
                                                                                        in_menu,
                                                                                        asked2, vk,
                                                                                        city_rand2)
            if event.message.text == 'Расстояния' or lens:
                try:
                    event, vk, lens, in_menu, first_place, renew = func_distance(event, vk, lens,
                                                                                 in_menu, first_place,
                                                                                 renew)
                except Exception as err:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                     message=f'Произошла ошибка. Вы находитесь в меню.')
                    showing_place = False
                    playing_cities = False
                    geocoding = False
                    guessing_city = False
                    first_place = False
                    in_menu = True
                    lens = False
                    city = None
                    asked = False
                    asked2 = False
                    asked_type = False
            if in_menu and not (event.message.text == 'zen' or event.message.text == 'пасхалка'):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                 message=f'Я SpaceBot и у меня есть множество функций. Их всех ты сейчас видишь на клавиатуре.')


if __name__ == '__main__':
    main()
