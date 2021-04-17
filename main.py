import requests
import vk_api
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
from functions import func_sp, func_pc, func_gc, func_gs, func_pt


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
                in_menu = True
                lens = False
                city = None
                asked = False
                asked2 = False
                asked_type = False
            # навыки:
            if event.message.text == 'Покажи место' or showing_place:
                try:
                    showing_place, asked, asked_type, city, in_menu = func_sp(event, asked, asked_type, city,
                                                                              vk, showing_place, in_menu)
                except Exception as a:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
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

            if event.message.text == 'Геокодер' or geocoding:
                try:
                    event, asked1, vk, geocoding, in_menu = func_gc(event, asked1, vk, geocoding, in_menu)
                except Exception as a:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
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
            if event.message.text == 'Игра в города' or playing_cities:
                try:
                    event, playing_cities, started, city_last, vk, in_menu, played_cities = func_pc(event, playing_cities, started, city_last, vk, in_menu, played_cities)
                except Exception as a:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
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
            if event.message.text == 'Угадай город' or guessing_city:
                try:
                    event, guessing_city, in_menu, asked2, vk, city_rand2 = func_gs(event, guessing_city, in_menu, asked2, vk, city_rand2)
                except Exception as a:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
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
            if event.message.text == 'Расстояния' or lens:
                try:
                    event, vk, lens, in_menu, first_place, renew = func_pt(event, vk, lens, in_menu, first_place, renew)
                except Exception as a:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
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
            if in_menu:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
                                 message=f'Я SpaceBot и у меня есть множество функций. Их всех ты сейчас видишь на клавиатуре.')


if __name__ == '__main__':
    main()
