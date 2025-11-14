
from wtforms import Form, StringField, PasswordField, validators ,ValidationError
from wtforms.validators import InputRequired, EqualTo

import re


''' Custom Validators '''

def hasLowercaseLetter(form, field):
    if not re.search(r'[a-z]', field.data):
            raise ValidationError('Field must contain at least one lowercase letter.')
            
def hasUppercaseLetter(form, field):
    if not re.search(r'[A-Z]', field.data):
            raise ValidationError('Field must contain at least one uppercase letter.')

def hasNumber(form, field):
    if not re.search(r'[0-9]', field.data):
            raise ValidationError('Field must contain at least one digit (0-9).')

def hasSpecialCharacter(form, field):
    if not re.search(r'[!@#$%^?]', field.data):
            raise ValidationError('Field must contain at least one special character (!@#$%^?).')


class RegistrationForm(Form):
    username = StringField('Username', [
        InputRequired(),
        validators.Length(min=4, message='Username should be at least 4 characters.'),
        validators.Length(max=25, message='Username cannot be more than 25 characters.')
    ])
    name = StringField('Name', [
        InputRequired(),
        validators.Length(min=1, message='Name should be at least 1 characters.'),
        validators.Length(max=25, message='Name cannot be more than 25 characters.')
    ])
    password = PasswordField('Password', [
        InputRequired(),
        validators.Length(min=8, max=25),
        EqualTo('confirm_password', 'Passwords must match.'),
    ])
    confirm_password = PasswordField('Confirm Password', [
        InputRequired(),
        EqualTo('password', 'Passwords must match.'),
        hasLowercaseLetter,
        hasUppercaseLetter,
        hasNumber,
        hasSpecialCharacter,
    ])

class LoginForm(Form):
    username = StringField('Username', [
        InputRequired(),
    ])
    password = PasswordField('Password', [
        InputRequired(),
    ])