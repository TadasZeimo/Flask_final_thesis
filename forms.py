from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class AddClimbers(FlaskForm):
    fname = StringField('Name:', [DataRequired()])
    lname = StringField('Last Name:', [DataRequired()])
    fotoUrl = StringField('Photo URL link:', [DataRequired()])
    biography = TextAreaField('')
    submit = SubmitField('Add')

class RegisterForm(FlaskForm):
    userName = StringField('User name:', [DataRequired()])
    email = EmailField('Email:', [DataRequired()])
    password1 = PasswordField('Password:', [DataRequired()])
    password2 = PasswordField('Repeat pass:', [DataRequired()])
    submit = SubmitField('Add User')

class LoginForm(FlaskForm):
    userName = StringField('User name:', [DataRequired()])
    password = PasswordField('Password:', [DataRequired()])
    chekbox = BooleanField('Remember me')
    submit = SubmitField('Login')