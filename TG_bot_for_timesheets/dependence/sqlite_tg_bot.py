import os, sys

# sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения содержимого папки Google_sheets_extension


# print(sys.path)

import dependence.sqlite_handler as lite

import telegram

class tgbot_db(lite.handler):
    def __init__(self, path) -> None:
        super().__init__(path)

    def get_user(update : telegram.update.Update): # Функция получения данных о пользователе
        userInfo = update.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
        userInfo = {'id': userInfo.id, 'first_name': userInfo.first_name, 'username': userInfo.username} # Получаем из объекта класса 'telegram.chat.Chat' словарь нужных нам значений

        return userInfo # Возвращаем данные о пользователе

    def set_newUser(self, update : telegram.update.Update):
        userInfo = update.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
        values = f"{userInfo.id}, '{userInfo.first_name}'"
        self.insert(table_name='user',coloms='user_id, user_fname', values=values)

    def set_userSheetId(self, update : telegram.update.Update):
        #  self.sql_cursor.execute(f'UPDATE {table_name} SET {colom} = {value} where {condition}')
        userInfo = update.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
        
        condition = f"user_id = {userInfo.id}"
        try:
            self.updata(table_name='user', colom='user_sheet_id', value=int(update.message.text), condition=condition)
        except Exception:
            update.message.reply_text( text='Something gone wrong !') 

def main():
    DB_PATH          = 'tg_bot.db'
    obj = tgbot_db(DB_PATH)

if __name__ == '__main__': # Если файл tg_bot.py вызаван, то будет запущен main(strBotToken); Если он будет импортироват то ничего не произайдёт
    main()

print(f'{__name__} is here !')