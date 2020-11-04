import telebot
from PIL import Image
from telebot import types

bot = telebot.TeleBot('1183729558:AAHWpXkzptfk35D76HWL1emyzUfrqQv1gas')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        '''Добро пожаловать. ✌ ''', reply_markup=keyboard())


@bot.message_handler(content_types=["text"])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'Погода':
        text = 'Не верь синоптикам'
        bot.send_message(chat_id, text, reply_markup=keyboard())
    elif message.text == 'Развлечения':
        text = 'Посмотрим, что у меня есть для тебя!'
        bot.send_message(chat_id, text, reply_markup=keyboard())
    elif message.text == 'Фото':
        with open("D:\phooto.jpg", "rb") as file:
            data = file.read()
            text = 'Фоточка'
        bot.send_photo(message.from_user.id, photo=data)
        bot.send_message(chat_id, text, reply_markup=keyboard())
    elif message.text == 'Аудио':
        audio = open('D:\music.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
        text = 'Музычка'
        bot.send_message(chat_id, text, reply_markup=keyboard())


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Погода')
    btn2 = types.KeyboardButton('Развлечения')
    btn3 = types.KeyboardButton('Фото')
    btn4 = types.KeyboardButton('Аудио')
    markup.add(btn1, btn2, btn3, btn4)
    return markup


if __name__ == "__main__":
    bot.polling(none_stop=True)
