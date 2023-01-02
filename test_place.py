l = [
        {
            'email':'CPTStol@yandex.ru',
            'subject':'Test',
            'text':'Test massage'
        },
        {
            'email':'majorstol@gmail.com',
            'subject':'Test',
            'text':'Test massage'
        },
        {
            'email':'pushihin@inbox.ru',
            'subject':'Test',
            'text':'Test massage'
        }
    ]  

# for dicts in l:
#     for item in dicts.values():
#         print(item, ' ')
#     print('\n')

for dicts in l:
    items = dicts.values()
    print(list(items), type(list(items)))

#     # CPTStol@yandex.ru
#     # majorstol@gmail.com
#     # pushihin@inbox.ru

import json_handler

json_handler.new_json('email_data.json',l)

print (json_handler.read_json('email_data.json'))