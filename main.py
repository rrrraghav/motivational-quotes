import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5  # pip install Bootstrap-Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import Session

from data_manager import DataManager

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

data_manager = DataManager()
quote = data_manager.get_quote()
author = data_manager.get_author()


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
        db.session.close_all()  # TODO: still doesnt work
        first_name = request.form['First Name']
        last_name = request.form['Last Name']
        user_email = request.form['Email']
        with app.app_context():
            new_customer = UserData(fn=first_name, ln=last_name, email=user_email)
            db.session.add(new_customer)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('form.html', form=form)


with app.app_context():
    result = db.session.execute(db.select(UserData))
    all_users = result.scalars()

if __name__ == '__main__':
    app.run(debug=True)
