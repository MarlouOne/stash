# import pandas
from pprint import pprint

import sys
import os
sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем 
import json_handler as jh

def get_list(file_name : str) -> list:
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read()
        data = data.split(' ')
        data[-1] = data[-1][:-1]
    return data
        
def set_dict(emails : list, subject : str, text : str, attachment : list, html : str) -> list:
    list_summary = []
    for email in emails:
        list_summary.append(             
                                {
                                    "email": email,
                                    "subject": subject,
                                    "text": text,
                                    "attachment": attachment,
                                    "html": html
                                }
                            )
    return list_summary
        
def main(file_name : str, subject : str, text : str, attachment : list, html : str):
    emails = get_list(file_name)
    # pprint(emails)
    emails = set_dict(emails, subject, text, attachment, html)
    # pprint(emails)
    jh.add_json('auto_email\emails_json.json', emails)
    
main('auto_email\src\школы без дубликатов.txt', "Приглашение на олимпиаду от Военно-космической академии имени А.Ф.Можайского", '', [], "auto_email\VKA.html")

            # {
            #     "email": "majorstol@gmail.com",
            #     "subject": "Приглашение на олимпиаду от Военно-космической академии имени А.Ф.Можайского",
            #     "text": "",
            #     "attachment": ["auto_email\VKA.html"],
            #     "html": "auto_email\VKA.html"
            # }