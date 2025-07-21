from __future__ import annotations

import logging

from flask import Blueprint, render_template, redirect, url_for

from ..services.booking_service import BookingService
from ..utils import login_required, role_required, setup_logger
from ..forms import BookingForm
from ..models import db, Booking

bp = Blueprint('bookings', __name__, url_prefix='/bookings')
logger = setup_logger(__name__, 'bookings.log')


@bp.route('/board')
@login_required
def reservation_board() -> str:
    """Display all bookings."""
    bookings = db.session.query(Booking).all()
    return render_template('board.html', bookings=bookings)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
def new_booking():
    """Create a booking."""
    form = BookingForm()
    if form.validate_on_submit():
        BookingService.create_booking(
            form.user_id.data, form.room_id.data, form.start_date.data, form.end_date.data
        )
        return redirect(url_for('bookings.reservation_board'))
    return render_template('new_booking.html', form=form)


@bp.route('/checkin/<int:bid>')
@login_required
def check_in(bid: int):
    BookingService.check_in(bid)
    return redirect(url_for('bookings.reservation_board'))


@bp.route('/checkout/<int:bid>')
@login_required
def check_out(bid: int):
    BookingService.check_out(bid)
    return redirect(url_for('bookings.reservation_board'))

