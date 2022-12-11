import os, sys

# sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения содержимого папки Google_sheets_extension


# print(sys.path)

import dependence.sqlite_handler as lite

import telegram

class tgbot_db(lite.handler):
    def __init__(self, path) -> None:
        super().__init__(path)

    def get_user(update : telegram.update.Update): # Функция получения данных о пользователе
        userInfo = update.callback_query.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
        userInfo = {'id': userInfo.id, 'first_name': userInfo.first_name, 'username': userInfo.username} # Получаем из объекта класса 'telegram.chat.Chat' словарь нужных нам значений

        return userInfo # Возвращаем данные о пользователе

    def set_newUser(self, update : telegram.update.Update):
        try:
            userInfo = update.callback_query.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
            values = f"{userInfo.id}, '{userInfo.first_name}'"
            self.insert(table_name='users',coloms='user_id, user_fname', values=values)
        except Exception:
            update.message.reply_text( text='Something gone wrong !') 

    def set_userSheetId(self, update : telegram.update.Update):
        #  self.sql_cursor.execute(f'UPDATE {table_name} SET {colom} = {value} where {condition}')
        userInfo = update.message.chat # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
        
        condition = f"user_id = {userInfo.id}"
        try:
            self.updata(table_name='users', colom='user_sheet_id', value=int(update.message.text), condition=condition)
        except Exception:
            update.message.reply_text( text='Something gone wrong !') 
    
    def check_userExistence(self, update : telegram.update.Update) -> bool: # Функция проверки существования записи о пользоавтеле. Если он сущетвует 1, иначе 0
        userID = update.callback_query.message.chat.id # Работает. Возвращает содержимое словаря "chat" -> id , first_name, type, username
        # self.sql_cursor.execute(f'SELECT {coloms} FROM {table_name} WHERE {condition}')
        condition = f"user_id = {userID}"
        result =  self.selectFromWhere(coloms='user_id', table_name="users", condition=condition)
        # print(result, len(result))

        
        return (len(result) != 0)

def main():
    DB_PATH          = 'bot.db'
    obj = tgbot_db(DB_PATH)

if __name__ == '__main__': # Если файл tg_bot.py вызаван, то будет запущен main(strBotToken); Если он будет импортироват то ничего не произайдёт
    main()

print(f'{__name__} is here !')