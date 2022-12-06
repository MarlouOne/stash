import os
from random import randint

content = os.listdir ('.\Telegram_bot\src') # C:\Users\major\Documents\GitHub\stash\Telegram_bot\tg_bot.py  C:\Users\major\Documents\GitHub\stash\Telegram_bot\src
print(content)

path = '.\Telegram_bot\src'
content = os.listdir (path) # C:\Users\major\Documents\GitHub\stash\Telegram_bot\tg_bot.py  C:\Users\major\Documents\GitHub\stash\Telegram_bot\src
photoPath = path + '\\' + content[randint(0,len(content)-1)]
print(photoPath)