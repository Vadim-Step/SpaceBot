import requests
import vk_api
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json


def main():
    vk_session = vk_api.VkApi(
        token='3de9c0ce56bb265632da8c7348a37fe081ebd68d9744120f9da0108b82654974ccd938d58ceee8cc26b9c')
    longpoll = VkBotLongPoll(vk_session, '203395569')
    city = None
    asked = False
    asked1 = False
    greet = False
    asked_type = False
    in_menu = True
    asked2 = False
    guessing_city = False
    showing_place = False
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
                in_menu = True
                city = None
                asked = False
                asked2 = False
                asked_type = False
            # навыки:
            if event.message.text == 'Покажи место' or showing_place:
                if event.message.text == 'Покажи место':
                    showing_place = True
                    in_menu = False
                if asked:
                    city = event.message.text
                if city and asked_type:
                    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}&format=json"
                    response = requests.get(geocoder_request)
                    if response:
                        json_response = response.json()
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]
                        toponym_coodrinates = toponym["Point"]["pos"]
                        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coodrinates.split())}&spn=0.1,0.1&l={event.message.text}"
                        response = requests.get(map_request)
                        map_file = "static/map.png"
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('static/map.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         random_id=random.randint(0, 2 ** 64),
                                         message=f'Это {city}. Что вы ещё хотите увидеть?',
                                         keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                         attachment=attachment)
                        city = True
                        asked_type = False
                else:
                    if event.message.text and not city:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Место:',
                                         keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                        asked = True
                    elif asked or city:
                        asked_type = True
                        asked = False
                        city = event.message.text
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Тип карты:',
                                         keyboard=open('kb1.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
            if event.message.text == 'Игра в города' or playing_cities:
                cities = open('cities.txt').read().split('\n')
                if event.message.text == 'Игра в города':
                    city_last = None
                    playing_cities = True
                    started = False
                    played_cities = []
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Начинайте!',
                                     keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
                if event.message.text in cities and event.message.text not in played_cities:
                    if not city_last or city_last[-1] == event.message.text.lower()[0]:
                        played_cities.append(event.message.text)
                        last = event.message.text[-1]
                        count = -1
                        while last == 'ы' or last == 'ь' or last == 'ъ':
                            count -= 1
                            last = event.message.text[count]
                        letter_cities = []
                        for i in cities:
                            if i.startswith(last.upper()) and i not in played_cities:
                                letter_cities.append(i)
                        city_rand = random.choice(letter_cities)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=city_rand,
                                         keyboard=open('kb3.json', 'r',
                                                       encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                        city_last = city_rand
                        played_cities.append(city_last)
                        count = 0
                        while city_last[-1] == 'ы' or city_last[-1] == 'ь' or city_last[-1] == 'ъ':
                            count -= 1
                            city_last = city_last[0:count]

                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Не то!',
                                         keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                elif event.message.text not in cities and not in_menu:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Нет такого города!',
                                     keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
                elif event.message.text in played_cities:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Был такой город!',
                                     keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
                in_menu = False
            if event.message.text == 'Геокодер' or geocoding:
                if event.message.text == 'Геокодер':
                    geocoding = False
                    in_menu = False
                    asked1 = False
                if asked1 == 'Прямое геокодирование':
                    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={event.message.text}&format=json"
                    response = requests.get(geocoder_request)
                    if response:
                        json_response = response.json()
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]
                        toponym_coodrinates = toponym["Point"]["pos"]
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f'Координаты - {toponym_coodrinates}. Что-то ещё?',
                                         keyboard=open('kb4.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                        asked1 = False
                elif asked1 == 'Обратное геокодирование':
                    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={event.message.text}&format=json"
                    response = requests.get(geocoder_request)
                    if response:
                        json_response = response.json()
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f'Мето - {toponym["metaDataProperty"]["GeocoderMetaData"]["text"]}. Что-то ещё?',
                                         keyboard=open('kb4.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                        asked1 = False
                else:
                    if event.message.text and not geocoding:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Геокодирование:',
                                         keyboard=open('kb4.json', 'r', encoding='UTF-8').read(),
                                         random_id=random.randint(0, 2 ** 64))
                        geocoding = True
                        asked1 = True
                    elif asked1 or geocoding:
                        asked1 = event.message.text
                        if asked1 == 'Прямое геокодирование':
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message='Введите место:',
                                             keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                             random_id=random.randint(0, 2 ** 64))
                        else:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message='Введите координаты, например 30 60:',
                                             keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                             random_id=random.randint(0, 2 ** 64))
            if event.message.text == 'Угадай город' or guessing_city:
                if event.message.text == 'Угадай город':
                    guessing_city = True
                    in_menu = False
                    asked2 = False
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Игра "Угадай город". Ваша задача по картинке угадать город.',
                                     keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                     random_id=random.randint(0, 2 ** 64))
                cities = open('cities2.txt', encoding='UTF-8').read().split('\n')
                if asked2:
                    if event.message.text == city_rand2:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         random_id=random.randint(0, 2 ** 64),
                                         message=f'Правильно!',
                                         keyboard=open('kb3.json', 'r', encoding='UTF-8').read())
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         random_id=random.randint(0, 2 ** 64),
                                         message=f'Неправильно! Это же {city_rand2}',
                                         keyboard=open('kb3.json', 'r', encoding='UTF-8').read())
                    asked2 = False
                if not asked2:
                    city_rand2 = random.choice(cities)
                    print(city_rand2)
                    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city_rand2}&format=json"
                    response = requests.get(geocoder_request)
                    if response:
                        json_response = response.json()
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"]
                        toponym_coodrinates = toponym["Point"]["pos"]
                        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coodrinates.split())}&spn=0.005,0.005&l=map"
                        response = requests.get(map_request)
                        map_file = "static/map.png"
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('static/map.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         random_id=random.randint(0, 2 ** 64),
                                         message=f'Какой это город?',
                                         keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                         attachment=attachment)
                        asked2 = True
            if in_menu:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
                                 message=f'Я SpaceBot и у меня есть множество функций. Их всех ты сейчас видишь на клавиатуре.')


if __name__ == '__main__':
    main()
