from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, UUID, AnyOf

class ReservationForm(FlaskForm):
    book_id = StringField('Book ID', validators=[DataRequired(), UUID()])

class ReservationUpdateForm(FlaskForm):
    status = StringField('Status', validators=[DataRequired(), AnyOf(['confirmed', 'rejected'])])