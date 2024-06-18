from app.services.user_service import is_username_unique, is_email_unique
from wtforms.validators import ValidationError

def validate_username(form, field):
    if form.current_username != None and form.current_username == field.data:
        return
    if not is_username_unique(field.data):
        raise ValidationError('Username is already in use.')

def validate_email(form, field):
    if form.current_email != None and form.current_email == field.data:
        return
    if not is_email_unique(field.data):
        raise ValidationError('Email is already in use.')