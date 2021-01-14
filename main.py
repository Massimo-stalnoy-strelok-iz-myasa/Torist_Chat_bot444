import telebot
from telebot import types
import weather
import users
import places
import converter
import random




API_KEY = '1529888724:AAHxeU7A2Vl-8Ock0xiKuvd7c91dhpZV25s'


bot = telebot.TeleBot(API_KEY)

global_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
global_markup.row('Куда сходить', 'Обновление геолокации')
global_markup.row('Погода', 'Курс валют')

secreat_txt, query = '', ''


def get_geo(cid, var):
    if var == 0:
        location_btn = telebot.types.KeyboardButton('Разрешить использовать геолокацию', request_location=True)
        cancel_btn = telebot.types.KeyboardButton('Отмена')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row(cancel_btn, location_btn)

        bot.send_message(cid, 'Включите геоданные', reply_markup=markup)
    elif var == 1:
        cancel_btn = telebot.types.KeyboardButton('Отмена')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row(cancel_btn)

        bot.send_message(cid, 'Отправьте геопозицию через вложение', reply_markup=markup)


def ask_for_geo(cid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Использовать геоданные устройства", callback_data='0'))
    markup.add(types.InlineKeyboardButton("Выбрать геопозицию", callback_data='1'))

    bot.send_message(cid, 'Как обновить геолокацию?', reply_markup=markup)


def check_user(message):
    uid = message.from_user.id
    if message.from_user.id not in users.get_users().keys():  # если такого пользователя не существует
        users.add_user(uid)
        user = users.get_user(uid)


@bot.message_handler(commands=['start'])
def start_message(message):
    cid = message.chat.id
    check_user(message)
    bot.send_message(cid, 'Приветствую, чем могу быть полезен', reply_markup=global_markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global secreat_txt, arr_answer
    check_user(message)
    cid = message.chat.id
    uid = message.from_user.id

    user = users.get_user(uid)

    if message.text.lower() == 'привет':
        bot.send_message(cid, 'Привет, чем могу тебе помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(cid, 'До связи!')
    elif message.text.lower() == 'отмена':
        bot.send_message(cid, 'Чем ещё я могу помочь?', reply_markup=global_markup)
        # простые сообщения

    elif message.text.lower() == 'обновить геолокацию':
        ask_for_geo(cid)
        # запрос геоданных

    elif message.text.lower() == 'куда сходить':
        if user.location == {}:  # если локация ещё не записана
            bot.send_message(cid, 'Повторите попытку после отправки геолокации')
            ask_for_geo(cid)
        else:
            # интересные места
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Все места поблизости", callback_data='0')
            item2 = types.InlineKeyboardButton("Рестораны и кафе 🍽️", callback_data='1')
            item3 = types.InlineKeyboardButton("Музеи 🏛️", callback_data='2')
            item4 = types.InlineKeyboardButton("Парки 🌳", callback_data='3')
            item5 = types.InlineKeyboardButton("Кино 🎥", callback_data='4')
            item6 = types.InlineKeyboardButton("Магазины 🛒", callback_data='5')
            markup.row(item1)
            markup.row(item2)
            markup.row(item3, item4)
            markup.row(item5, item6)

            bot.send_message(cid, 'Какие места найти? 🚶', reply_markup=markup)

    elif message.text.lower() == 'курс валют':
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Доллар $", callback_data='0')
        item5 = types.InlineKeyboardButton("Резервная валюта мира", callback_data='2')
        item2 = types.InlineKeyboardButton("Евро €", callback_data='1')
        item3 = types.InlineKeyboardButton("Английский фунт £", callback_data='3')
        item4 = types.InlineKeyboardButton("Швейцарский франк ₣", callback_data='4')
        markup.row(item1, item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(types.InlineKeyboardButton("Полная информация о курсах", callback_data='5'))

        bot.send_message(cid, 'Какая валюта вас интересует?', reply_markup=markup)

    elif message.text.lower() == 'погода':
        if user.location == {}: 
            bot.send_message(cid, 'Повторите попытку после отправки геолокации')
            ask_for_geo(cid)
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Погода сейчас", callback_data='0'))
            markup.add(types.InlineKeyboardButton("Подробная погода", callback_data='1'))
            markup.add(types.InlineKeyboardButton("Прогноз на 3 дня", callback_data='2'))

            bot.send_message(cid, 'Выберите вариант погоды ⛅', reply_markup=markup)

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIMA1-_elxUNoSiKjuUns_Lsi_QXoI0AAL1AAMw1J0R3NeLwV6aUvUeBA')


@bot.message_handler(content_types=['location'])
def handle_loc(message):
    check_user(message)
    cid = message.chat.id
    uid = message.from_user.id
    user = users.get_user(uid)

    bot.send_message(cid, 'Мы получили геолокацию', reply_markup=global_markup)
    user.location = message.location
    user.is_have_location = True
    users.save_users()


def send_places(call, user, cid):
    result = places.get_places(user, bot, call.message, int(call.data), 2)
    if result != 0:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Посмотреть ещё", callback_data=call.data))
        bot.send_message(cid, 'Хотите посмотреть ещё?', reply_markup=markup)


def get_places_for_opros(user):
    try:
        places.get_all_places(user)
        users.save_users()
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global secreat_txt, arr_answer, query
    cid = call.message.chat.id
    uid = call.from_user.id
    user = users.get_user(uid)
    max_num = 0

    try:
        if call.message.text == 'Какая валюта вас интересует?':
            print()
            if int(call.data) == 5:
                bot.send_message(cid,
                                 'Полная информация находится на сайте\n'
                                 ' https://www.banki.ru/products/currency/cash/moskva/#bank-rates')

            else:
                arr_valua = ['доллар', 'евро', 'резервная валюта мира', 'английский фунт', 'швейцарский франк']
                bot.send_message(cid, 'Курс валюты _{}_ \n*{:.2f}* рублей'.format(arr_valua[int(call.data)],
                                                                                  converter.converter_1(
                                                                                      int(call.data))),
                                 parse_mode='Markdown')

        elif call.message.text == 'Какие места найти? 🚶':
            send_places(call, user, cid)
        elif call.message.text == 'Хотите посмотреть ещё?':
            send_places(call, user, cid)
        elif call.message.text == 'Выберите вариант погоды ⛅':
            # weather.get_weather(user, bot, message)
            if int(call.data) == 0:
                weather.simple_weather(user, bot, call.message)
            if int(call.data) == 1:
                weather.detailed_weather(user, bot, call.message)
            if int(call.data) == 2:
                weather.three_days_weather(user, bot, call.message)

        elif call.message.text == 'Как обновить геолокацию?':
            get_geo(cid, int(call.data))
    except:
        pass


bot.polling()
