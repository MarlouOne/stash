d = {
    'CPTStol@yandex.ru':'Test massage',
    'majorstol@gmail.com':'Test massage',
    'pushihin@inbox.ru':'Test massage'
    }  

# for item in d.items():
#     print(item)

#     # CPTStol@yandex.ru
#     # majorstol@gmail.com
#     # pushihin@inbox.ru

import json_handler

json_handler.new_json('email_data.json',d)

print (json_handler.read_json('email_data.json'))