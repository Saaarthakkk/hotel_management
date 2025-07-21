from __future__ import annotations

import logging
import os

from flask import Blueprint, render_template, redirect, url_for

from ..services.booking_service import BookingService
from ..utils import login_required, role_required

bp = Blueprint('bookings', __name__, url_prefix='/bookings')
logger = logging.getLogger(__name__)
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'bookings.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
handler = logging.FileHandler(log_path)
logger.addHandler(handler)


@bp.route('/board')
@login_required
def reservation_board():
    """Display all bookings."""
    bookings = BookingService.list_bookings()
    return render_template('board.html', bookings=bookings)


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
