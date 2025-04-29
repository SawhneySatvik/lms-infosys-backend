from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import Optional, Length, Email

class LibrarianUpdateForm(FlaskForm):
    name = StringField('Name', validators=[Optional(), Length(min=2, max=100)])
    email = StringField('Email', validators=[Optional(), Email()])
    is_active = BooleanField('Is Active', validators=[Optional()])