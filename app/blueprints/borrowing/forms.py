from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, UUID

class BorrowForm(FlaskForm):
    reservation_id = StringField('Reservation ID', validators=[DataRequired(), UUID()])

class ReturnForm(FlaskForm):
    borrow_id = StringField('Borrow ID', validators=[DataRequired(), UUID()])