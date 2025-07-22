# PLAN: provide creation, edit and search forms for rooms and bookings.
from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    PasswordField,
    BooleanField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RoomForm(FlaskForm):
    """Simple room creation form."""

    number = StringField('Number', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])


class BookingForm(FlaskForm):
    """Booking creation form with dynamic room lookup."""

    user_id = SelectField('Guest', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    """Admin user registration form."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])


class StaffRegistrationForm(FlaskForm):
    """Form for staff applications."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Work Email', validators=[DataRequired(), Email()])
    role = SelectField(
        'Role', choices=[('receptionist', 'Receptionist'), ('housekeeping', 'Housekeeping')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)],
    )
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
    agree = BooleanField('I agree to the code of conduct', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')


class EditRoomForm(FlaskForm):
    """Form for editing a room."""

    number = StringField('Number', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])


class EditBookingForm(FlaskForm):
    """Form for editing a booking."""

    guest_name = StringField('Guest', validators=[DataRequired()])
    start_date = DateField('Start', validators=[DataRequired()])
    end_date = DateField('End', validators=[DataRequired()])


class SearchBookingForm(FlaskForm):
    """Form for searching bookings."""

    guest_name = StringField('Guest')
    start_date = DateField('Start', format='%Y-%m-%d')
    end_date = DateField('End', format='%Y-%m-%d')

