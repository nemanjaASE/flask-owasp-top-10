from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectMultipleField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Post')