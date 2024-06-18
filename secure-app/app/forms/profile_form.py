from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from app.forms.validators.user_validator import validate_username, validate_email

class ProfileForm(FlaskForm):
    current_username = None
    current_email = None
    
    username = StringField('Username', validators=[DataRequired(), Length(max=24), validate_username])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=24)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=24)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=32), validate_email])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    submit = SubmitField('Save')