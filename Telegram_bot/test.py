import os
from random import randint

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
from random import randint

import sys, os

sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения содержимого папки Google_sheets_extension
import Google_sheets_extension.Google_sheet_extension_v2

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton

import inspect


content = os.listdir ('.\Telegram_bot\src') # C:\Users\major\Documents\GitHub\stash\Telegram_bot\tg_bot.py  C:\Users\major\Documents\GitHub\stash\Telegram_bot\src
print(content)

path = '.\Telegram_bot\src'
content = os.listdir (path) # C:\Users\major\Documents\GitHub\stash\Telegram_bot\tg_bot.py  C:\Users\major\Documents\GitHub\stash\Telegram_bot\src
photoPath = path + '\\' + content[randint(0,len(content)-1)]
print(photoPath)

file_info = bot.get_file(message.photo[0].file_id)
downloaded_file = bot.download_file(file_info.file_path)

src = filepath + message.photo[0].file_id
with open(src, 'wb') as new_file:
    new_file.write(downloaded_file)