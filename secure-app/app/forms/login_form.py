from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class LoginForm(FlaskForm):
    recaptcha = RecaptchaField()

    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=32),
        Email()])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=64, message='Password must be between 8 and 64 characters long.'),
        Regexp(r'^[A-Za-z\d@$!%*?&]{8,64}$', message="Password can only contain letters, numbers, and special characters @$!%*?&.")])
    
    submit = SubmitField('Login')