from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

class DeleteUserForm(FlaskForm):
    user_id = HiddenField('User ID')
    submit = SubmitField('Delete')