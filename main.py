import os
import random
import smtplib

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

my_email = os.environ['EMAIL']
email_password = os.environ['PASSWORD']
app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ['SECRETKEY']

random_page_num = random.randint(1, 100)
URL = f'https://www.goodreads.com/quotes/tag/motivational?page={random_page_num}'

response = requests.get(URL)
site = response.text
soup = BeautifulSoup(site, 'html.parser')

quotes = soup.find_all(name='div', class_='quoteText')
quote_list = [quote.get_text().strip().split('\n')[0] for quote in quotes]
authors = soup.find_all(name='span', class_='authorOrTitle')
author_list = [author.get_text().strip().title().split(',')[0] for author in authors]

quote = random.choice(quote_list)
index = quote_list.index(quote)
author = author_list[index]


@app.route('/')
def home():
    return render_template('index.html', quote=quote, author=author)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def mailing_list():
    return render_template('form.html')


with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=email_password)
    connection.sendmail(from_addr=my_email, to_addrs='coding1email@yahoo.com',
                        msg=f'Subject: Quote of the Day\n\n{quote} - {author}'.encode())


if __name__ == '__main__':
    app.run(debug=True)
