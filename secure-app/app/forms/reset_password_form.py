from flask_wtf import FlaskForm
from app.services.pwned_service import PwnedService
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')

    def __init__(self, pwned_service: PwnedService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pwned_service = pwned_service

    def validate_password(self, password_field):
        password = password_field.data
        
        if len(password) < 8 or len(password) > 64:
            raise ValidationError('Password must be between 8 and 64 characters long.')

        if self.pwned_service.is_password_compromised(password):
            raise ValidationError('Password is compromised and cannot be used.')