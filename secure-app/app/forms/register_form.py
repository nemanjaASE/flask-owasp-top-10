from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.services.pwned_service import PwnedService
from app.forms.validators.user_validator import validate_username, validate_email

class RegistrationForm(FlaskForm):
    current_username = None
    current_email = None
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=24)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=24)])
    username = StringField('Username', validators=[DataRequired(),Length(max=24), validate_username])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=32), validate_email])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=64, message='Password must be between 8 and 64 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    birth_date = DateField('Birth Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Register')

    def __init__(self, pwned_service: PwnedService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pwned_service = pwned_service

    def validate_password(self, password_field):
        password = password_field.data
        if len(password) < 8 or len(password) > 64:
            raise ValidationError('Password must be between 8 and 64 characters long.')

        if self.pwned_service.is_password_compromised(password):
            raise ValidationError('Password is compromised and cannot be used.')
