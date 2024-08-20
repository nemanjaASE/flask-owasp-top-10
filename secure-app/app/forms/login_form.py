from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    recaptcha = RecaptchaField()
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=32)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')