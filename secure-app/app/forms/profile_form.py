from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from app.forms.validators.user_validator import validate_username, validate_email

class ProfileForm(FlaskForm):
    current_username = None
    current_email = None
    
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(max=24), 
        Regexp(r'^[\w]+$', message='Username can only contain letters, numbers, and underscores'), 
        validate_username])
    
    first_name = StringField('First Name', validators=[
        DataRequired(), 
        Length(max=24),
        Regexp(r'^[A-Za-z\s]+$', message='First name can only contain letters and spaces.')])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(), 
        Length(max=24),
        Regexp(r'^[A-Za-z\s]+$', message='Last name can only contain letters and spaces.')])
    
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(), 
        Length(max=32), 
        validate_email])
    
    birth_date = DateField('Birth Date', validators=[
        DataRequired()],
        format='%Y-%m-%d')
    
    submit = SubmitField('Save')