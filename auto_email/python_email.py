import smtplib
# import dependence.json_handler as json_handler
from email.message import EmailMessage
import imghdr

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

    def broadcast_json(self, file_path : str) -> None : # Рассылка множество писем по данным из json файла
        data = json_handler.read_json(file_path)
        for dicts in data:
            items = list(dicts.values())
            m = massage(self)
            m.set_content(items[0], items[1], items[2])
            m.set_attachment(items[3])
            m.send_mail()
    
    def broadcast_cache(self, data : list) -> None :  # Рассылка множество писем по данным из словаря
        for dicts in data:
            items = list(dicts.values())
            m = massage(self)
            m.set_content(items[0], items[1], items[2])
            m.set_attachment(items[3])
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
    
    def set_attachment(self, file_path) -> None:
        with open(file_path, 'rb') as attachment:
            image_data = attachment.read()
            image_type = imghdr.what(attachment.name)
            image_name = attachment.name
        self.msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

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
    man = postman('majorstol@gmail.com', 'datwdfqcebyanyup')
    man.self_check()

    l = [
            {
                "email": "CPTStol@yandex.ru",
                "subject": "Test - Тест",
                "text": "Test massage - Тескстовое сообщение",
                "attachment": "auto_email\Daddy.jpg"
            },
            {
                "email": "majorstol@gmail.com",
                "subject": "Test - Тест",
                "text": "Test massage - Тескстовое сообщение",
                "attachment": "auto_email\Daddy.jpg"
            },
            {
                "email": "pushihin@inbox.ru",
                "subject": "Test - Тест",
                "text": "Test massage - Тескстовое сообщение",
                "attachment": "auto_email\Daddy.jpg"
            },
            {
                "email": "g.jarkovskij@yandex.ru",
                "subject": "For Goga - Заголовок",
                "text": "Derji papku ! - Тескстовое сообщение",
                "attachment": "auto_email\Daddy.jpg"
            },
        ]           

    man.broadcast_cache(l)

    # man.broadcast_json('python_email\email_data.json')

    man.drop_service()

if __name__ == '__main__': 
    main()

print(f'{__name__} is here !')