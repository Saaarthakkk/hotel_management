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
