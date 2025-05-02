from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, UUID

class WishlistForm(FlaskForm):
    book_id = StringField('Book ID', validators=[DataRequired(), UUID()])