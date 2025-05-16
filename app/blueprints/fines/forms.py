from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional, UUID

class FineForm(FlaskForm):
    borrow_id = StringField('Borrow ID', validators=[DataRequired(), UUID()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    reason = StringField('Reason', validators=[DataRequired()])

class FineUpdateForm(FlaskForm):
    is_paid = BooleanField('Is Paid', validators=[Optional()])