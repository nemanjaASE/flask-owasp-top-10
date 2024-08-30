from app.repositories.user_repository import UserRepository
from wtforms.validators import ValidationError

user_repo = UserRepository()

def validate_username(form, field):
    if form.current_username != None and form.current_username == field.data:
        return
    if not user_repo.is_username_unique(field.data):
        raise ValidationError("The provided credentials are already in use. Please choose a different username or email.")

def validate_email(form, field):
    if form.current_email != None and form.current_email == field.data:
        return
    if not user_repo.is_email_unique(field.data):
        raise ValidationError('The provided credentials are already in use. Please choose a different username or email.')