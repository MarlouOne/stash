# Use this token to access the HTTP API:
# 5620370083:AAGu5OcD-59_sNmPevlZqq8AplOxJkGKwR0

# t.me/Small_test_project_bot

from pprint import pprint

import logging

logging.basicConfig(filename='./Telegram_bot/bot.log', level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s" ) # Логгируем ВСЕ сообщения в файл "bot.log" по формату <Врмемя Тип сообщения Сообщение>

import inspect

def showVarType(var) -> None: # Узнаём тип данных произвольной переменной
    caller_locals = inspect.currentframe().f_back.f_locals
    varName = [name for name, value in caller_locals.items() if var is value] # Получаем имя переменной 
    print(var, f'\n{varName} type is {type(var)}') # Узнаём тип данных переменной 

import settings # Импортируем "защищенный" файл с "важной" информацией

strBotToken = settings.API_KEY # Токен из "защищенного" файла settings.py

CREDENTIALS_FILE = 'pythonextension-202bab519501.json'  # Файла "pythonextension-202bab519501.json", содержащий закрытый ключ 

path = '.\Telegram_bot\src' # Путь к папке с фотографиями

import sys, os

sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения содержимого папки Google_sheets_extension
import Google_sheets_extension.Google_sheet_extension_v2

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton

# def generat_KeyboardButton( listButtons : list) -> None: # Функция генерации новых кнопок на панели
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Создаём разметку
#     for strButtons in listButtons: 
#         btn = types.KeyboardButton( text=strButtons) # Создаём кнопу с конкретным название
#         markup.add(btn) # Добавляем кнопку в разметку
#     return markup # Возвращаем разметку

# def generat_InlineButtons( dictButtons : dict) -> None: # Функция генерации новых контекстных кнопок 
#     markup = types.InlineKeyboardMarkup() # Создаём разметку
#     for dictButton in dictButtons:
#         btn = types.InlineKeyboardButton(text=dictButton, callback_data=dictButtons[dictButton]) # Создаём кнопу с конкретным название и значением обратного ответа
#         markup.add(btn) # Добавляем кнопку в разметку
#     return markup # Возвращаем разметку

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
from random import randint
# from telegram.ext import *

def get_user(update : telegram.update.Update): # Функция получения данных о пользователе
    """
    print(dict(update)) # Не работает
    print(str(update)) # Работает
    print(update.get('message')) # Не работает
    print(update.getRawResponse()) # Не работает
    
    # print(update.message.chat) # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
    """

    userInfo = update.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username

    # print(userInfo, f'\nuserInfo type is {type(userInfo)}') # Узнаём тип данных переменной userInfo -> telegram.chat.Chat

    userInfo = {'id': userInfo.id, 'first_name': userInfo.first_name, 'username': userInfo.username} # Получаем из объекта класса 'telegram.chat.Chat' словарь нужных нам значений

    # print(userInfo, f'\nuserInfo type is {type(userInfo)}') # Узнаём тип данных переменной userInfo -> dict

    return userInfo # Возвращаем данные о пользователе

def func_start(update : telegram.update.Update, context): # Функция обработки команды "/start"
    print("Funcion 'start' was colled !")
    logging.info("Funcion 'start' was colled !")
    # print("Update :\n", update, f'\nUpdate type is {type(update)}', "\nContext :\n", context, f'\nContext type is {type(context)}')

    userInfo = get_user(update) # Получаем информацию о пользователе

    showVarType(update)
    showVarType(context)
    

    # print(userInfo.items()) # Не работает

    subText = ''
    for key, value in userInfo.items(): # Формируем строку информации о пользователе
        subText += str(key).capitalize() + ' - ' + str(value) + '\n'

    # print(subText, showVarType(subText)) # Тип -> str
    
    replyText = f'Hi user !\nInformation about you :\n{subText}' # Формируем строку ответа пользователю

    # print(replyText, showVarType(replyText)) # Тип -> str

    update.message.reply_text(replyText) # Ответ пользователю в чате telegram

def send_echoMessage(update : telegram.update.Update, context) -> None: # Функция, которая отвечат пользователю тем же сообщение текстовым которое он отправил
    print("Funcion 'send_echoMessage' was colled !")
    logging.info("Funcion 'send_echoMessage' was colled !")

    replyText = update.message.text # Получаем текстовое сообщени пользователя 
    print(f'Users text is "{replyText}"') 
    update.message.reply_text(replyText) # Ответ пользователю в чате telegram

def send_randomPhoto(update : telegram.update.Update, path : str) -> None: # Функция, которая отправляет случайнуюю фотографию из папки "src"
    print("Funcion 'send_randomPhoto' was colled !")
    logging.info("Funcion 'send_randomPhoto' was colled !")
    # print(update)

    content = os.listdir (path) # C:\Users\major\Documents\GitHub\stash\Telegram_bot\tg_bot.py  C:\Users\major\Documents\GitHub\stash\Telegram_bot\src
    photoPath = path + '\\' + content[randint(0,len(content)-1)]

    # print(photoPath)

    img = {'photo': open(photoPath, 'rb')}

    # print(img)

    update.callback_query.message.reply_photo(photo=img['photo'], caption='Regular photo')

def set_echoInLineButton(update : telegram.update.Update, context): # Функция вывода на экран кнопки с введенным пользователем текстом
    print("Funcion 'set_echoButton' was colled !")
    logging.info("Funcion 'set_echoButton' was colled !")

    message = update.message.text # Получаем текстовое сообщени пользователя 
    keyboard = [ [ InlineKeyboardButton(message, callback_data='echoCallback'), InlineKeyboardButton('Send random photo', callback_data='send_randomPhoto') ] ] # Создаём кнопку с введённым текстом
    markup = InlineKeyboardMarkup(keyboard) # Создаём разметку с полученной кнопкой
    
    # update.message.bot.send_message( text='Echo should be button is here !') # Не работает
    # update.message.bot.send_message(chat_id = update.message.chat_id, text='Echo button is here !', reply_markup = markup) # Не работает
    # update.bot.send_message(chat_id = update.message.chat_id, text='Echo button is here !', reply_markup = markup) # Не работает
    # context.bot.send_message(chat_id = update.message.chat_id, text='Echo button is here !', reply_markup = markup) # Не работает
    
    update.message.reply_text( text='Echo button should be is here !') 
    update.message.reply_text( text='Echo button is here !', reply_markup = markup) # Выводим кнопку в чат 

def set_echoKeyboardButton(update : telegram.update.Update, context): # Функция вывода на панель кнопки с введенным пользователем текстом
    print("Funcion 'set_echoKeyboardButton' was colled !")
    logging.info("Funcion 'set_echoKeyboardButton' was colled !")
    keyboard = [ [ KeyboardButton('Case 1'), KeyboardButton('Case 2') ] ] # Создаём кнопку с введённым текстом | Нет параметра "Callback_data" 
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True, one_time_keyboard = True, input_field_placeholder = "Keyboard :")
    update.message.reply_text( text='___', reply_markup = markup)# Выводим кнопку в чат 
    # update.message.bot.delete_message(update.message.chat.id, update.message.message_id)

def callbackHandler(update: Update, context): # Функция обработки обаратных запросов (callback_data)
    global path
    print("Funcion 'callbackHandler' was colled !")
    logging.info("Funcion 'callbackHandler' was colled !")
    query = update.callback_query.data # Вычленяем обаратный запрос (callback_data)
    logging.info(f"Query - '{query}' !")
    
    print(f"Query - '{query}' !")

    if query == 'echoCallback':
        echoCallback(update) # Ручка для обработки "callback_data='echoCallback'"
    elif query == 'send_randomPhoto':
        send_randomPhoto(update, path)

def echoCallback(update: Update): # Функция отправки окна с сообщением по нажатию кнопки с "callback='echoCallback'"
    print("Funcion 'echoCallback' was colled !")
    logging.info("Funcion 'echoCallback' was colled !")
    query = update.callback_query # Информационное сообщение в виде словаря словарей 
    # showVarType(update) # -> telegram.update.Update'
    # print("query :", query) 
    # showVarType(query) # -> telegram.callbackquery.CallbackQuery
    data = query.data # Callback, который был передан в результате действия (например - нажатия кнопки)
    # print('data :', data)
    # showVarType(data) # -> str
    replyText = f'This is echo button callback - {data}!' # Создаём информационное сообщение 
    # update.message.reply_text( text = replyText ) # Не работает
    update.callback_query.answer(replyText, show_alert=True) # Выводим ответ на экран <=> query.answer(replyText) 
    query.message.reply_text(replyText) # Выводим ответ в чат

def textHandler(update : telegram.update.Update, context): # Функция обработки текстовых сообщений
    print("Funcion 'textHandler' was colled !")
    logging.info("Funcion 'textHandler' was colled !")
    # contentText = update.message.text
    # print(update.message.message_id)
    # print(contentText)

    # if contentText == "--TODEL" : 
    #     # update.messagedelete_message(message.chat.id,message.message_id)
    #     update.message.bot.delete_message(update.message.chat.id, update.message.message_id)

    send_echoMessage(update, context)
    set_echoInLineButton(update, context)
    set_echoKeyboardButton(update, context)

def photoHandler(update : telegram.update.Update, context): # Функция обработки сообщений с фотографиями
    global path 

    print("Funcion 'photoHandler' was colled !")
    logging.info("Funcion 'photoHandler' was colled !")

    file_info = update.message.bot.get_file(update.message.photo[-1].file_id) # Получаем вариант фотографии из сообщения с максимальным разрешением 
    file_info.download(path + '\download' + f'\{update.message.photo[-1].file_id}.png') # Скачиваем фотографию из сообщения в указанное место

def googleSheets_handler(update):
    print("Funcion 'googleSheets_handler' was colled !")
    logging.info("Funcion 'googleSheets_handler' was colled !")

    message = update.message.text # Получаем текстовое сообщени пользователя 
    message = message.split('\n')
    print(message)

    if message[0] == '':
        print(message[0])

def set_commandHandlers(mybot : Updater): # Функция обявляет ручки для диспетчра 
    dp = mybot.dispatcher # Создаём объект <Диспетчер>

    dp.add_handler(CommandHandler('start', func_start)) # Ручка для команды "/start"
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
    main(strBotToken)