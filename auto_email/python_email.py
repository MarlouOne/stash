import smtplib
# import dependence.json_handler as json_handler
from email.message import EmailMessage
import imghdr

from mimetypes import MimeTypes
from urllib.request import pathname2url
from email.mime.text import MIMEText

import sys
import os
sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем 
import json_handler

class postman():
    post_service : smtplib.SMTP
    email : str


    def __init__(self, email : str, password : str ) -> None: 
        try:
            self.email = email
            self.post_service = smtplib.SMTP('smtp.gmail.com', 587)
            # self.post_service = smtplib.SMTP('smtp.gmail.com', 587)
        
            self.post_service.starttls()
            self.post_service.login(email , password)
        except Exception:
            print(f"--- Can`t connect {email} with password {password}")
        else:
            print(f'--- Connected to {email} with password {password}')
        

    def self_check(self) -> None: # Отправка письма на свой адрес для проверки работоспособности сеанса рассылки
        self.post_service.sendmail(self.email, self.email, 'This message sended by python script !')

    def send_mail(self, receiver_email : str, massage : str) -> None: # Отправка письма по адресу "receiver_email" с содержимым "massage"
        try :
            self.post_service.sendmail(self.email, receiver_email, massage.encode('utf-8'))
        except Exception:
            print(f'--- Can`t delevery message to {receiver_email}')
        else:
            print(f'--- Message delivered message to {receiver_email}')

    def drop_service(self) -> None: # Завершение сеанса рассылки
        self.post_service.quit()
        print(f'--- Session closed')

    def broadcast(self, content) -> None :  # Рассылка множество писем по данным из словаря
        if type(content) == str:
            data = json_handler.read_json(content)
        else : 
            data = content
            
        for dicts in data:
            m = massage(self)
            m.set_content(dicts["email"], dicts["subject"], dicts["text"])
            m.set_attachment(dicts["attachment"])
            m.set_html(dicts["html"])
            m.send_mail()
    
    


class massage(postman):
    msg : EmailMessage
    man : postman

    def __init__(self, man : postman) -> None:
        self.msg = EmailMessage()
        self.man = man
        self.msg['From'] = self.man.email

    def set_text(self, text : str) -> None:
        self.msg.set_content(text)
    
    def set_subject(self, subject : str) -> None:
        self.msg['Subject'] = subject

    def set_receiver_email(self, receiver_email : str) -> None:
        self.msg['To'] = receiver_email
    
    def get_maintype(self, file_path : str) -> list:
        mime = MimeTypes()
        url = pathname2url(file_path)
        return ( mime.guess_type(url) )[0].split('/')

    def set_attachment(self, list_files) -> None:
        for file_path in list_files:
            with open(file_path, 'rb') as attachment:
                file_data = attachment.read()
                file_type =  self.get_maintype(file_path)
                file_name = attachment.name
                self.msg.add_attachment(file_data, maintype=file_type[0], subtype=file_type[1], filename=file_name.split('.')[0])

    def set_html(self, html_file : str) -> None:
        try:
            with open(html_file, 'r', encoding='utf-8') as html:
                file_data = html.read()
                self.msg.attach(MIMEText(file_data, "html"))
                
        except Exception:
            print('Error in setting HTML')

    def set_content(self, receiver_email : str, subject : str, text : str) -> None:
        self.set_receiver_email(receiver_email)
        self.set_subject(subject)
        self.set_text(text)
    

    def send_mail(self) -> None:
        try :
            self.man.post_service.send_message(self.msg)
        except Exception:
            print(f'--- Can`t delevery message to {self.msg["To"]}')
        else:
            print(f'--- Message delivered message to {self.msg["To"]}')

def main():
    man = postman('majorstol@gmail.com', 'datwdfqcebyanyup') # Создаём сессию "EP"
    # man.self_check() # Проверка работоспособности соединения сессии

    l = [
            # {
            #     "email": "CPTStol@yandex.ru",
            #     "subject": "Test - Тест",
            #     "text": "Test massage - Тескстовое сообщение",
            #     "attachment": ["auto_email\IMAGE 2023-01-19 22_43_10.pdf"],
            #     "html": "auto_email\Test.html"
            # },
            {
                "email": "g.jarkovskij@yandex.ru",
                "subject": "Test - Тест",
                "text": "Test massage - Тескстовое сообщение",
                "attachment": ["auto_email\steam.html"],
                "html": "auto_email\VKA.html"
            }
            # },
            # {
            #     "email": "pushihin@inbox.ru",
            #     "subject": "Test - Тест",
            #     "text": "Test massage - Тескстовое сообщение",
            #     "attachment": ["auto_email\IMAGE 2023-01-19 22_43_10.pdf", "auto_email\Test.html"],
            #     "html": "auto_email\Test.html"
            # },
            # {
            #     "email": "g.jarkovskij@yandex.ru",
            #     "subject": "For Goga - Заголовок",
            #     "text": "Derji papku ! - Тескстовое сообщение",
            #     "attachment": ["auto_email\IMAGE 2023-01-19 22_43_10.pdf", "auto_email\Test.html"],
            #     "html": "auto_email\Test.html"
            # },
        ]           

    man.broadcast(l)

    # man.broadcast_json('python_email\email_data.json')

    man.drop_service()

if __name__ == '__main__': 
    main()

print(f'{__name__} is here !')