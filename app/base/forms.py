# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', id='pwd_login',
            validators=[DataRequired()])
    new_password = PasswordField('New Password', id='pwd_login',
            validators=[DataRequired()])
    password_confirmation = PasswordField('Password Confirmation', id='pwd_login',
            validators=[DataRequired()])
