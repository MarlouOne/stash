import smtplib
import dependence.json_handler as json_handler

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
        for item in data.items():
            self.send_mail(item[0], item[1])
    
    def broadcast_dict(self, data : dict) -> None :  # Рассылка множество писем по данным из словаря
        for item in data.items():
            self.send_mail(item[0], item[1])

TEXT = 'Мужчины и Дамы, тут будет обсуждаться план проведения очередного Нового года. \n Все будут услышаны, поэтому предлагайте свои идеи !'

def main():
    man = postman('majorstol@gmail.com', 'datwdfqcebyanyup')
    man.self_check()

    d = {
    'CPTStol@yandex.ru':'Test massage from dict',
    'majorstol@gmail.com':'Test massage from dict',
    'pushihin@inbox.ru':'Test massage from dict'
    }  

    man.broadcast_dict(d)

    # man.send_mail('majorstol@gmail.com',TEXT) # \n Бабы are temporary !
    # man.send_mail('pushihin@inbox.ru','[хуй] is eternal !') # \n Бабы are temporary !
    # man.send_mail('CPTStol@yandex.ru','[хуй] is eternal !') # \n Бабы are temporary !

    man.broadcast_json('email_data.json')


    man.drop_service()
    
# main()




# smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

# smtpObj.starttls()

# smtpObj.login('majorstol@gmail.com','datwdfqcebyanyup')

# smtpObj.sendmail("majorstol@gmail.com","majorstol@gmail.com","go to bed!")

# smtpObj.quit()


if __name__ == '__main__': 
    main()

print(f'{__name__} is here !')