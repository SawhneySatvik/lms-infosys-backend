from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError, Optional
from ...models.users import User
from ...models.libraries import Library
from ...models.otp_verifications import OTPVerification
import uuid
from datetime import datetime, timedelta, timezone  # Added timezone import

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters'),
        Regexp(r'^(?=.*[A-Z])(?=.*\d)', message='Password must contain at least one uppercase letter and one number')
    ])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    library_id = StringField('Library ID', validators=[DataRequired()])
    user_image = FileField('User Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Sign Up')

    def validate_library_id(self, library_id):
        try:
            uuid_obj = uuid.UUID(library_id.data)
        except ValueError:
            raise ValidationError('Invalid library_id format. Must be a valid UUID.')
        library = Library.query.filter_by(library_id=library_id.data).first()
        if not library:
            raise ValidationError('Library does not exist.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class OTPForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    otp = StringField('OTP', validators=[DataRequired(), Length(min=6, max=6, message='OTP must be 6 characters')])
    submit = SubmitField('Verify OTP')

    def validate_user_id(self, user_id):
        try:
            uuid_obj = uuid.UUID(user_id.data)
        except ValueError:
            raise ValidationError('Invalid user_id format. Must be a valid UUID.')
        user = User.query.filter_by(user_id=user_id.data).first()
        if not user:
            raise ValidationError('User not found.')

    def validate_otp(self, otp):
        user = User.query.filter_by(user_id=self.user_id.data).first()
        if not user:
            return

        # Check attempt count
        recent_attempts = OTPVerification.query.filter(
            OTPVerification.user_id == self.user_id.data,
            OTPVerification.created_at >= datetime.now(timezone.utc) - timedelta(minutes=15)  # Updated
        ).count()
        if recent_attempts >= 3:
            raise ValidationError('Too many failed OTP attempts. Please try again after 15 minutes.')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(min=2, max=100)])
    email = StringField('Email', validators=[Email()])
    user_image = FileField('User Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Update Profile')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class RefreshTokenForm(FlaskForm):
    refresh_token = StringField('Refresh Token', validators=[DataRequired()])
    submit = SubmitField('Refresh Token')

class AdminRegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters'),
        Regexp(r'^(?=.*[A-Z])(?=.*\d)', message='Password must contain at least one uppercase letter and one number')
    ])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    user_image = FileField('User Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    library_name = StringField('Library Name', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=100)])
    pincode = IntegerField('Pincode', validators=[DataRequired()])
    submit = SubmitField('Register Admin')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')

    def validate_library_name(self, library_name):
        if Library.query.filter_by(name=library_name.data).first():
            raise ValidationError('Library name already exists.')

class LibrarianRegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters'),
        Regexp(r'^(?=.*[A-Z])(?=.*\d)', message='Password must contain at least one uppercase letter and one number')
    ])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    user_image = FileField('User Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Register Librarian')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')