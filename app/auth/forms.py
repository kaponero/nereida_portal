# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, TextAreaField
from wtforms.validators import Email, DataRequired

## login

class LoginForm(FlaskForm):
    email = TextField('email', id='email_login',
            validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_login',
            validators=[DataRequired()])
