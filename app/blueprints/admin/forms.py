from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField
from wtforms.validators import Optional, NumberRange

class SettingsForm(FlaskForm):
    fine_rate = DecimalField('Fine Rate', validators=[Optional(), NumberRange(min=0)])
    max_borrow_days = IntegerField('Max Borrow Days', validators=[Optional(), NumberRange(min=1)])