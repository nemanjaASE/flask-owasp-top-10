from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp

class OTPForm(FlaskForm):
   otp_1 = StringField('', validators=[
        DataRequired(),
        Regexp('^[0-9]$'),
    ], render_kw={"maxlength": "1"})

   otp_2 = StringField('', validators=[
        DataRequired(),
        Regexp('^[0-9]$'),
    ], render_kw={"maxlength": "1"})

   otp_3 = StringField('', validators=[
        DataRequired(),
        Regexp('^[0-9]$'),
    ], render_kw={"maxlength": "1"})

   otp_4 = StringField('', validators=[
        DataRequired(),
        Regexp('^[0-9]$'),
    ], render_kw={"maxlength": "1"})

   otp_5 = StringField('', validators=[
        DataRequired(),
        Regexp('^[0-9]$'),
    ], render_kw={"maxlength": "1"})

   otp_6 = StringField('', validators=[
        DataRequired(),
        Regexp('^[0-9]$'),
    ], render_kw={"maxlength": "1"})
    
   submit = SubmitField('Submit')