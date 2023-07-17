import os
import pandas
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5  # pip install Bootstrap-Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from data_manager import DataManager
from email_manager import EmailManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRETKEY']
bootstrap = Bootstrap5(app)


class EmailForm(FlaskForm):
    first_name = StringField(name='First Name', validators=[DataRequired()])
    last_name = StringField(name='Last Name', validators=[DataRequired()])
    email = StringField(name='Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


data_manager = DataManager()
quote = data_manager.get_quote()
author = data_manager.get_author()

email_manager = EmailManager()


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
        first_name = request.form['First Name'].title()
        last_name = request.form['Last Name'].title()
        user_email = request.form['Email']
        user_data = f'\n{first_name},{last_name},{user_email}'
        with open('customer-data.csv', mode='a') as file:
            file.write(user_data)
        return redirect(url_for('home'))
    return render_template('form.html', form=form)


user_info = pandas.read_csv('customer-data.csv')
email_list = user_info['email']
for email in email_list:
    row = user_info[user_info.email == email]
    name = str(row.fn).split('    ')[1].split('\n')[0]
    email_manager.send_email(email, quote, author, name)

if __name__ == '__main__':
    app.run(debug=True)
