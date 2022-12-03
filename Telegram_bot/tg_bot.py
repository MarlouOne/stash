# Use this token to access the HTTP API:
# 5620370083:AAGu5OcD-59_sNmPevlZqq8AplOxJkGKwR0

# t.me/Small_test_project_bot

import logging

logging.basicConfig(filename='bot.log', level=logging.INFO )


import inspect

def showVarType(var) -> None: # Узнаём тип данных произвольной переменной
    caller_locals = inspect.currentframe().f_back.f_locals
    varName = [name for name, value in caller_locals.items() if var is value] # Получаем имя переменной 
    print(var, f'\n{varName} type is {type(var)}') # Узнаём тип данных переменной 


strBotToken = '5620370083:AAGu5OcD-59_sNmPevlZqq8AplOxJkGKwR0'

from telegram.ext import Updater, CommandHandler

def get_user(update): # Функция получения данных о пользователе
    """
    print(dict(update)) # Не работает
    print(str(update)) # Работает
    print(update.get('message')) # Не работает
    print(update.getRawResponse()) # Не работает
    
    # print(update.message.chat) # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
    """

    userInfo = update.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username

    print(userInfo, f'\nuserInfo type is {type(userInfo)}') # Узнаём тип данных переменной userInfo -> telegram.chat.Chat

    userInfo = {'id': userInfo.id, 'first_name': userInfo.first_name, 'username': userInfo.username} # Получаем из объекта класса 'telegram.chat.Chat' словарь нужных нам значений

    print(userInfo, f'\nuserInfo type is {type(userInfo)}') # Узнаём тип данных переменной userInfo -> dict

    return userInfo # Возвращаем данные о пользователе

def set_commandHandlers(mybot): # Функция обявляет ручки для диспетчра 
    dp = mybot.dispatcher # Создаём объект <Диспетчер>

    dp.add_handler(CommandHandler('start', func_start)) # Ручка для команды "/start"

    return dp # Возвращаем диспетчер со всеми "ручками"

def func_start(update, context): # Функция обработки команды "/start"
    print("Funcion 'start' was colled !")
    print("Update :\n", update, f'\nUpdate type is {type(update)}', "\nContext :\n", context, f'\nContext type is {type(context)}')

    userInfo = get_user(update) # Получаем информацию о пользователе

    # print(userInfo.items()) # Не работает

    subText = ''
    for key, value in userInfo.items(): # Формируем строку информации о пользователе
        subText += str(key).capitalize() + ' - ' + str(value) + '\n'

    # print(subText, showVarType(subText)) # Тип -> str
    
    replyText = f'Hi user !\nInformation about you :\n{subText}' # Формируем строку ответа пользователю

    # print(replyText, showVarType(replyText)) # Тип -> str

    update.message.reply_text(replyText) # Ответ пользователю в чате telegram
    

def main(strBotToken):
    mybot = Updater(strBotToken, use_context=True) 

    dp = set_commandHandlers(mybot) # Создаём объект <Диспетчер>

    mybot.start_polling() # Бот начинает обращатся к серверу telegram
    mybot.idle() # бот работает пока работает хост
    
    print('Bot is alive !') # Выводим в консоль что бот запущен

    

main(strBotToken)