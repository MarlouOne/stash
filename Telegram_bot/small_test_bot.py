# Use this token to access the HTTP API:
# 5620370083:AAGu5OcD-59_sNmPevlZqq8AplOxJkGKwR0

# t.me/Small_test_project_bot

strBotToken = '5620370083:AAGu5OcD-59_sNmPevlZqq8AplOxJkGKwR0'

# import pandas as pd
# import support_function as sf
import telebot 

bot = telebot.TeleBot(strBotToken)

from telebot import types



# df = sf.get_df()
# print(df)

def generat_KeyboardButton( listButtons : list) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
    for strButtons in listButtons:
        btn = types.KeyboardButton( text=strButtons) # print(dictButton, dictButtons[dictButton]) Ключ - значение
        markup.add(btn)
    return markup

def generat_InlineButtons( dictButtons : dict) -> None:
    markup = types.InlineKeyboardMarkup() #создание новых кнопок
    for dictButton in dictButtons:
        btn = types.InlineKeyboardButton(text=dictButton, callback_data=dictButtons[dictButton]) # print(dictButton, dictButtons[dictButton]) Ключ - значение
        markup.add(btn)
    return markup


print('Bot was hosted')

@bot.message_handler(commands=['start']) # Запуск бота

def start(message: types.Message):
    print('A new session has been started...')
    dictInlineButtons = {
                        'Turn on the bot !' :  'online'
                        }
                        
    markup = generat_InlineButtons(dictInlineButtons)
    bot.send_message(message.chat.id, "Bot is offline !", reply_markup=markup)
    # message.answer("Bot is offline !", reply_markup=markup)

                    # 'Turn on the bot !' :  'online'

@bot.callback_query_handler(func=lambda call: call.data == 'online')

# @bot.callback_query_handler(func=lambda call: True)
# @bot.callback_query_handler(func=lambda call: call.message == 'select_phone')

def select_mode(call): # , message: types.Message
    print('User now in choose mode!')
    print(call.data)
    dictInlineButtons = {
                    'Do you want to select a phone ?' :  'select_phone',
                    'Do you want to generate a cringe ?' : 'generate_cringe'
                  }
    markup = generat_InlineButtons(dictInlineButtons)
    bot.send_message(call.message.chat.id, "Make your choise :", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'select_phone')

def select_phone(message: types.Message, call):
    print('User now in select phone mode!')
    # dfLocal = df
    
    strColor  = ""
    strMemory = ""
    strType   = ""
    strModel  = ""
    
    dictInlineButtons = {
                    'Select color' :  'select_color',
                    'Select memory count' :  'select_memory',
                    'Select phone type' :  'select_type',
                    'Select phone model' :  'select_model',
                    'Find an offer' : 'make_choice',
                    'Back' : 'online'
                    }
    markup = generat_KeyboardButton(list(dictInlineButtons))
    bot.send_message(call.message.chat.id, "Find an offer :", reply_markup=markup)

    # while True:
    #     if message.text == 'Select color':
    #         print('select_color')
    #         listColors = sf.get_listUniqueValues(dfLocal, 'color')
    #     elif message.text == 'Select memory count':
    #         print('select_memory')
    #         listMemory = sf.get_listUniqueValues(dfLocal, 'memory')
    #     elif message.text == 'Select phone type':
    #         print('select_type')
    #         listColors = sf.get_listUniqueValues(dfLocal, 'type')
    #     elif message.text == 'Select phone model':
    #         print('select_model')
    #         listColors = sf.get_listUniqueValues(dfLocal, 'model')
    #     elif message.text == 'Back':
    #         print('Back')
    #         call.data = 'online'

    # while call.data != 'online':
    #     if call.data == 'select_color':
    #         print('select_color')
    #         listColors = sf.get_listUniqueValues(dfLocal, 'color')

    #     if call.data == 'select_memory':
    #         print('select_memory')
    #         listMemory = sf.get_listUniqueValues(dfLocal, 'memory')

    #     if call.data == 'select_type':
    #         print('select_type')
    #         listColors = sf.get_listUniqueValues(dfLocal, 'type')

    #     if call.data == 'select_model':
    #         print('select_model')
    #         listColors = sf.get_listUniqueValues(dfLocal, 'model')



    # bot.send_message(message.chat.id, "Select the mode you need :", reply_markup=markup)
    # message.answer("Select the mode you need :", reply_markup=markup)

# @bot.message_handler(lambda message: message.text == "Без пюрешки") # для клавиатурных кнопок 

# @bot.callback_query_handler(text="select_phone")

# def select_phone(call: types.CallbackQuery):
#      call.message.answer(call.message.text)

# @bot.callback_query_handler(text="generate_cringe")

# def generate_cringe(call: types.CallbackQuery):
#      call.message.answer(call.message.text)
    







#     markup = buttonGenerator(dictButtons)
#     bot.send_message(message.from_user.id, "Bot is offline", reply_markup=markup)
    
# @bot.callback_query_handler(func=lambda call: call.data == "online") 
# # @bot.callback_query_handler(func=lambda call: call.data == "button1")

# def select_mode(message, call: types.CallbackQuery):
#     dictButtons = {
#                     'Do you want to pick up a phone' :  'pick_up'
#                   }
#     print('User now in choose mode!')
#     bot.send_message(message.from_user.id, "Bot is offline", reply_markup=markup)
#     markup = buttonGenerator(dictButtons)

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть


# @bot.message_handler(content_types=['text'])

# def get_text_messages(message):
#     if message.text == 'Turn on the bot !':
#         markup = buttonGenerator({'Choose an Iphone': None})
#         bot.send_message(message.from_user.id, "Bot is online", reply_markup=markup)

# # Обработчик нажатий на кнопки
# @bot.callback_query_handler(func=lambda call: True)

# def callback_worker(call):
#     pass

# @bot.message_handler(commands=["Choose an Iphone"])

# def set_Choose(message):
#     bot.send_message(message.from_user.id, "Select the parameters you need :")
#     dictBottons = {'Color':'Color','Memory':'Memory'}
#     markup = buttonGenerator({'': None})
#     print('User now in choose mode!')

"""
@bot.message_handler(commands=['start'])

def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])

def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Как стать автором на Хабре?')
        btn2 = types.KeyboardButton('Правила сайта')
        btn3 = types.KeyboardButton('Советы по оформлению публикации')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота


    elif message.text == 'Как стать автором на Хабре?':
        bot.send_message(message.from_user.id, 'Вы пишете первый пост, его проверяют модераторы, и, если всё хорошо, отправляют в основную ленту Хабра, где он набирает просмотры, комментарии и рейтинг. В дальнейшем премодерация уже не понадобится. Если с постом что-то не так, вас попросят его доработать.\n \nПолный текст можно прочитать по ' + '[ссылке](https://habr.com/ru/sandbox/start/)', parse_mode='Markdown')

    elif message.text == 'Правила сайта':
        bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)', parse_mode='Markdown')

    elif message.text == 'Советы по оформлению публикации':
        bot.send_message(message.from_user.id, 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', parse_mode='Markdown')


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
"""