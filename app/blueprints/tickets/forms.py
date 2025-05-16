from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Optional, AnyOf

class TicketForm(FlaskForm):
    type = StringField('Type', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    priority = StringField('Priority', validators=[Optional(), AnyOf(['low', 'medium', 'high'])])

class TicketUpdateForm(FlaskForm):
    status = StringField('Status', validators=[DataRequired(), AnyOf(['open', 'in_progress', 'resolved'])])