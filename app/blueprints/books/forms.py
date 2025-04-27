from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, Optional
from uuid import UUID

class UUIDListField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = [UUID(val) for val in valuelist[0].split(',') if val]
            except ValueError:
                self.data = []
                raise ValueError('Invalid UUID format')
        else:
            self.data = []

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=255)])
    isbn = StringField('ISBN', validators=[Optional(), Length(min=10, max=13), Regexp(r'^\d{10}(\d{3})?$')])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    publisher_name = StringField('Publisher', validators=[Optional(), Length(max=255)])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    book_image = FileField('Book Image', validators=[Optional()])
    author_ids = UUIDListField('Author IDs', validators=[Optional()])
    genre_ids = UUIDListField('Genre IDs', validators=[Optional()])
    published_date = StringField('Published Date', validators=[Optional(), Regexp(r'^\d{4}-\d{2}-\d{2}$')])

class BookUpdateForm(BookForm):
    total_copies = IntegerField('Total Copies', validators=[Optional(), NumberRange(min=1)])