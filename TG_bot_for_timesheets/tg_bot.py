# Use this token to access the HTTP API:
# 5620370083:AAGu5OcD-59_sNmPevlZqq8AplOxJkGKwR0

# t.me/Small_test_project_bot


import src.settings as settings # Импортируем "защищенный" файл с "важной" информацией

BOT_TOKEN        = settings.API_KEY # Токен из "защищенного" файла settings.py
DB_PATH          = './TG_bot_for_timesheets/src/bot.db'
CREDENTIALS_FILE = '../src/pythonextension-202bab519501.json'  # Файла "pythonextension-202bab519501.json", содержащий закрытый ключ 


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
import telegram.ext


def start(update : telegram.update.Update, context : telegram.ext.callbackcontext.CallbackContext):

    print("Funcion 'start' was colled !")
    logging.info("Funcion 'start' was colled !")
    
    keyboard = [ [ InlineKeyboardButton('Let`s start !', callback_data='startCallback')] ] # Создаём кнопку с введённым текстом
    markup = InlineKeyboardMarkup(keyboard) # Создаём разметку с полученной кнопкой
    update.message.reply_text( text='Bot is online !', reply_markup = markup) # Выводим кнопку в чат 
    context.user_data['status'] = 'Free' # Записываем сосояние без конкретной привязки к действиям пользователя 
    print(f'Context -', context.user_data['status'])

def login(update : telegram.update.Update, context : telegram.ext.callbackcontext.CallbackContext):

    print("Funcion 'login' was colled !")
    logging.info("Funcion 'login' was colled !")

    print(context.user_data['status'])

    # showVarType(update)
    # userInfo = update.message.chat

    if DB_handler.check_userExistence(update) == False: # Проверяем есть ли такой пользователь в базе данных
        print(f'User with id = {update.callback_query.message.chat.id} not existe')
        DB_handler.set_newUser(update)
        print(f'User with id = {update.callback_query.message.chat.id} now in db')

        set_GoogleSheetID(update, context)
    else: # Такой пользователь уже есть
        print(f'User with id = {update.callback_query.message.chat.id} was existe in db')
    
        keyboard = [ [ InlineKeyboardButton('Yes', callback_data='set_GoogleSheetID'),  InlineKeyboardButton('No', callback_data='use_extention')] ] # Создаём кнопку с введённым текстом
        markup = InlineKeyboardMarkup(keyboard) # Создаём разметку с полученной кнопкой
        update.callback_query.message.reply_text( text='Do you want to change your Google Sheet ID ?', reply_markup = markup) # Выводим кнопку в чат 
    
        # update.callback_query.message.reply_text(text='Looks like you already was here. \n Please enter your Google sheet ID !', reply_markup = markup )

def set_GoogleSheetID(update : telegram.update.Update, context : telegram.ext.callbackcontext.CallbackContext): # Записываем новую ссылку на Google Sheet
    print("Funcion 'set_GoogleSheetID' was colled !")
    logging.info("Funcion 'set_GoogleSheetID' was colled !")

    context.user_data['status'] = 'set_GoogleSheetID' # Записываем сосояние ожидания ввода Google Sheet ID
    old_ID = str(DB_handler.get_userSheetId(update))
    keyboard = [ [ KeyboardButton(old_ID) ] ] # Создаём кнопку с введённым текстом | Нет параметра "Callback_data" 
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True, one_time_keyboard = True, input_field_placeholder = "Enter your Google sheet ID here:") # Создаём разметку с полученной кнопкой
    update.callback_query.message.reply_text( text='Please enter your Google sheet ID !', reply_markup = markup) # Выводим кнопку в чат;  Остаток текста - Looks like you already was here. \n 
    # showVarType(old_ID)

def insert_Google_Sheet_ID(update : telegram.update.Update, context : telegram.ext.callbackcontext.CallbackContext):
    print(f"Funcion 'textHandler' was colled with context status {context.user_data['status']} !")
    logging.info(f"Funcion 'textHandler' was colled with context status {context.user_data['status']}")

    DB_handler.set_userSheetId(update)
    status = GSE.extension(CREDENTIALS_FILE = CREDENTIALS_FILE, sheet_id= DB_handler.get_userSheetId(update)).status

    print(DB_handler.get_userSheetId(update))
    print(status)

    if GSE.extension(CREDENTIALS_FILE = CREDENTIALS_FILE, sheet_id= DB_handler.get_userSheetId(update)).is_connected() == True:
        update.message.reply_text(text='The bot has successfully connected to your Google sheet !')
        context.user_data['status'] = 'Free' # Записываем сосояние без конкретной привязки к действиям пользователя 
    else:
        update.message.reply_text(text='The bot has successfully connected to your Google sheet !')
        DB_handler.set_userSheetId(update)



def callbackHandler(update : telegram.update.Update, context : telegram.ext.callbackcontext.CallbackContext): # Функция обработки обаратных запросов (callback_data)
    global path
    print("Funcion 'callbackHandler' was colled !")
    logging.info("Funcion 'callbackHandler' was colled !")
    query = update.callback_query.data # Вычленяем обаратный запрос (callback_data)
    logging.info(f"Query - '{query}' !")
    
    # showVarType(context)

    print(f"Query - '{query}' !")

    if query == 'startCallback':
        login(update, context)
    elif query == 'set_GoogleSheetID':
        set_GoogleSheetID(update, context)

def textHandler(update : telegram.update.Update, context : telegram.ext.callbackcontext.CallbackContext): # Функция обработки текстовых сообщений

    
    print(f"Funcion 'textHandler' was colled with context status {context.user_data} !")
    logging.info(f"Funcion 'textHandler' was colled with context status {context.user_data} !")

  
    status = context.user_data['status']
    print(status == 'set_GoogleSheetID')
    showVarType(status)

    if status == 'set_GoogleSheetID':
        print("Go to insert_Google_Sheet_ID !")
        insert_Google_Sheet_ID(update, context)
    

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