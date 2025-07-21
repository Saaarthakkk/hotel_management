# PLAN: provide creation, edit and search forms for rooms and bookings.
from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    """Simple room creation form."""

    number = StringField('Number', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])


class BookingForm(FlaskForm):
    """Simple booking creation form."""

    user_id = StringField('User ID', validators=[DataRequired()])
    room_id = StringField('Room ID', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])


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

