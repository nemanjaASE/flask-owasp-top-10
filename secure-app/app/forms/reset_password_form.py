from flask_wtf import FlaskForm
from app.services.pwned_service import PwnedService
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp
from app.services.exceptions.invalid_input_exception import InvalidInputException

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=64, message='Password must be between 8 and 64 characters long.'),
        Regexp(r'^[A-Za-z\d@$!%*?&]{8,64}$', message="Password can only contain letters, numbers, and special characters @$!%*?&.")])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        Length(min=8, max=64, message='Password must be between 8 and 64 characters long.'),
        Regexp(r'^[A-Za-z\d@$!%*?&]{8,64}$', message="Password can only contain letters, numbers, and special characters @$!%*?&."),
        EqualTo('password')])
    
    submit = SubmitField('Reset')

    def __init__(self, pwned_service: PwnedService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pwned_service = pwned_service

    def validate_password(self, field):
        password = field.data

        if not password:
            raise ValidationError("Password cannot be empty")
        try:
            if self.pwned_service.is_password_compromised(password):
                raise ValidationError('Password is compromised and cannot be used.')
        except (InvalidInputException, Exception) as e:
            return e