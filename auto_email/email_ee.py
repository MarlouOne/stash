import smtplib
import os
from email.mime.text import MIMEText


def send_email():
    sender = 'majorstol@gmail.com'
    # your password = "your password"
    password = os.getenv('datwdfqcebyanyup')

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        with open("auto_email\steam.html", 'r', encoding='utf-8') as file:
            template = file.read()
            # print(template)
    except IOError:
        return "The template file doesn't found!"

    try:
        server.login(sender, password)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = sender
        msg["Subject"] = "С Днем Рождения! Только сегодня скидка по промокоду до 90%!"
        server.sendmail(sender, sender, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    print(send_email())


if __name__ == "__main__":
    main()