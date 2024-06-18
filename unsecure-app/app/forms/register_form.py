from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.forms.validators.user_validator import validate_username, validate_email

class RegistrationForm(FlaskForm):
    current_username = None
    current_email = None
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=24)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=24)])
    username = StringField('Username', validators=[DataRequired(), Length(max=24), validate_username])
    email = StringField('Email', validators=[DataRequired(), Email(),Length(max=32), validate_email])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    birth_date = DateField('Birth Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Register')