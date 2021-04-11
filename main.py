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
    greet = False
    asked_type = False
    in_menu = False
    showing_place = False
    playing_cities = False
    for event in longpoll.listen():
        vk = vk_session.get_api()
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not greet:
                response = vk.users.get(user_id=event.obj.message['from_id'])
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 message=f'Приветствую тебя, {response[0]["first_name"]}')
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
                                 message=f'Я SpaceBot и у меня есть множество функций. Их всех ты сейчас видишь на клавиатуре.')
                greet = True
            if event.message.text.lower() == 'выйти':
                showing_place = False
                playing_cities = False
                in_menu = True
                city = None
                asked = False
                asked_type = False
                print('yep')
            # навыки:
            if event.message.text == 'Покажи место' or showing_place:
                if event.message.text == 'Покажи место':
                    showing_place = True
                    in_menu = False
                print(event.message.text, showing_place)
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
                playing_cities = True
                in_menu = False
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Функция в разработке...',
                                 keyboard=open('kb3.json', 'r', encoding='UTF-8').read(),
                                 random_id=random.randint(0, 2 ** 64))
            if in_menu:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('kb2.json', 'r', encoding='UTF-8').read(),
                                 message=f'Я SpaceBot и у меня есть множество функций. Их всех ты сейчас видишь на клавиатуре.')


if __name__ == '__main__':
    main()