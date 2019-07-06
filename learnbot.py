# Импорты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

from glob import glob
import logging
from random import choice
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
# ответ на старт
def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет  {}'.format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard())

# Ответ той же фразой что написал пользователь
def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = 'Привет, {} {}! Ты написал {}'.format(update.message.chat.first_name, emo, update.message.text)
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username, update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

# отправляем код
def send_code_picture(bot, update, user_data):
    code_list = glob('images/code*.png')
    code_pic = choice(code_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(code_pic, 'rb'), reply_markup=get_keyboard())

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

def get_keyboard():
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать код', '/start', 'Hello', 'Сменить аватарку'],
        [contact_button, location_button]
    ], resize_keyboard=True
    )
    return my_keyboard

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(emo), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Спасибо {}'.format(get_avatar(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Спасибо {}'.format(get_avatar(user_data)), reply_markup=get_keyboard())

# Тело бота
def main():
    print('START')
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот Запустился')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("code", send_code_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать код)$', send_code_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()





main()