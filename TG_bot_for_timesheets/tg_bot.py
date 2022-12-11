# Use this token to access the HTTP API:
# 5620370083:AAGu5OcD-59_sNmPevlZqq8AplOxJkGKwR0

# t.me/Small_test_project_bot


import src.settings as settings # Импортируем "защищенный" файл с "важной" информацией

BOT_TOKEN        = settings.API_KEY # Токен из "защищенного" файла settings.py
DB_PATH          = './TG_bot_for_timesheets/src/bot.db'
CREDENTIALS_FILE = './TG_bot_for_timesheets/src/pythonextension-202bab519501.json'  # Файла "pythonextension-202bab519501.json", содержащий закрытый ключ 


from pprint import pprint
import logging
import inspect
import sys, os

# sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения их содержимого 

# pprint(sys.path)

import dependence.Google_sheet_extension_v3_in_class as GSE
import dependence.sqlite_tg_bot as STB

logging.basicConfig(filename='./TG_bot_for_timesheets/bot.log', level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s" ) # Логгируем ВСЕ сообщения в файл "bot.log" по формату <Врмемя Тип сообщения Сообщение>

def showVarType(var) -> None: # Узнаём тип данных произвольной переменной
    caller_locals = inspect.currentframe().f_back.f_locals
    varName = [name for name, value in caller_locals.items() if var is value] # Получаем имя переменной 
    print(var, f'\n{varName} type is {type(var)}') # Узнаём тип данных переменной 

# extention = GSE.extension(CREDENTIALS_FILE=CREDENTIALS_FILE,)

DB_handler = STB.tgbot_db(path=DB_PATH)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
# from telegram.ext import *


def start(update : telegram.update.Update, context):
    print("Funcion 'start' was colled !")
    logging.info("Funcion 'start' was colled !")
    
    keyboard = [ [ InlineKeyboardButton('Let`s start !', callback_data='startCallback')] ] # Создаём кнопку с введённым текстом
    markup = InlineKeyboardMarkup(keyboard) # Создаём разметку с полученной кнопкой
    update.message.reply_text( text='Bot is online !', reply_markup = markup) # Выводим кнопку в чат 

def login(update : telegram.update.Update, context):
    print("Funcion 'login' was colled !")
    logging.info("Funcion 'login' was colled !")

    # showVarType(update)
    # userInfo = update.message.chat

    if DB_handler.check_userExistence(update) == False:
        print(f'User with id = {update.callback_query.message.chat.id} not existe')
        DB_handler.set_newUser(update)
        print(f'User with id = {update.callback_query.message.chat.id} now in db')
    else:
        print(f'User with id = {update.callback_query.message.chat.id} was existe in db')
# def 

def callbackHandler(update: Update, context): # Функция обработки обаратных запросов (callback_data)
    global path
    print("Funcion 'callbackHandler' was colled !")
    logging.info("Funcion 'callbackHandler' was colled !")
    query = update.callback_query.data # Вычленяем обаратный запрос (callback_data)
    logging.info(f"Query - '{query}' !")
    
    print(f"Query - '{query}' !")

    if query == 'startCallback':
        login(update, context)


def textHandler(update : telegram.update.Update, context): # Функция обработки текстовых сообщений
    print("Funcion 'textHandler' was colled !")
    logging.info("Funcion 'textHandler' was colled !")

def photoHandler(update : telegram.update.Update, context): # Функция обработки сообщений с фотографиями
    global path 
    print("Funcion 'photoHandler' was colled !")
    logging.info("Funcion 'photoHandler' was colled !")

def set_commandHandlers(mybot : Updater): # Функция обявляет ручки для диспетчра 
    dp = mybot.dispatcher # Создаём объект <Диспетчер>

    dp.add_handler(CommandHandler('start', start)) # Ручка для команды "/start"
    dp.add_handler(MessageHandler(Filters.text, textHandler)) # Ручка для всего получаемого текста
    dp.add_handler(MessageHandler(Filters.photo, photoHandler)) # Ручка для всех получаемых фотографий
    dp.add_handler(CallbackQueryHandler(callbackHandler)) # Ручка для обработки различных callback_data
    return dp # Возвращаем диспетчер со всеми "ручками"

def main(strBotToken): # Функция основоного стека вызова
    mybot = Updater(strBotToken, use_context=True) # Создаём объект "mybot" класса "Updater" отвечающий за взаимодействие с сервером telegram

    dp = set_commandHandlers(mybot) # Создаём объект <Диспетчер>

    mybot.start_polling() # Бот начинает обращатся к серверу telegram
    
    print("-"*10,'\nBot is alive !') # Выводим в консоль что бот запущен
    logging.info('"Bot" is alive !')

    mybot.idle() # бот работает пока работает хост
    
if __name__ == '__main__': # Если файл tg_bot.py вызаван, то будет запущен main(strBotToken); Если он будет импортироват то ничего не произайдёт
    main(BOT_TOKEN)