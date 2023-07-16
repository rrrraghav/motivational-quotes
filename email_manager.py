import smtplib
import os

my_email = os.environ['EMAIL']
password = os.environ['PASSWORD']


class EmailManager:
    def __init__(self):
        self.my_email = my_email
        self.password = password

    def send_email(self, email, quote, author, name):
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(from_addr=self.my_email, to_addrs=email, msg='Subject: Quote of the Day\n\n'
                                                                             f'{quote} - {author}'
                                                                             f'\n Have a great day {name}!'
                                .encode('utf-8'))
