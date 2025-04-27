from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Optional

class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=255)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=1000)])
    author_image = FileField('Author Image', validators=[Optional()])