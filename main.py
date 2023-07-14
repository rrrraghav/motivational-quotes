import os
import random
import smtplib

import requests
import sqlalchemy
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5  # pip install Bootstrap-Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import Session

my_email = os.environ['EMAIL']
email_password = os.environ['PASSWORD']
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRETKEY']
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///customer-data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///customer-data.db')
session = Session(engine)
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)


class EmailForm(FlaskForm):
    first_name = StringField(name='First Name', validators=[DataRequired()])
    last_name = StringField(name='Last Name', validators=[DataRequired()])
    email = StringField(name='Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserData(db.Model):
    id = Column(Integer, primary_key=True)
    fn = Column(String, nullable=False)
    ln = Column(String, nullable=False)
    email = Column(String, nullable=False)


with app.app_context():
    db.create_all()

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


@app.route('/signup', methods=['GET', 'POST'])
def mailing_list():
    form = EmailForm()
    if form.validate_on_submit():
        first_name = request.form['First Name']
        last_name = request.form['Last Name']
        user_email = request.form['Email']
        with app.app_context():
            new_customer = UserData(fn=first_name, ln=last_name, email=user_email)
            try:
                db.session.add(new_customer)
                db.session.commit()
            except sqlalchemy.exc.OperationalError: # need to fix this still
                db.session.close_all()
        return redirect(url_for('home'))
    return render_template('form.html', form=form)


with app.app_context():
    result = db.session.execute(db.select(UserData))
    all_users = result.scalars()

if __name__ == '__main__':
    app.run(debug=True)
