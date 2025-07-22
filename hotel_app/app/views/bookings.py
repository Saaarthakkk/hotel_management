# PLAN: booking routes including CRUD and search features.
from __future__ import annotations

import logging

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from datetime import date

from ..services.booking_service import BookingService
from ..services.room_service import RoomService
from ..services.auth_service import AuthService
from ..utils import login_required, role_required, setup_logger
from ..forms import BookingForm, EditBookingForm, SearchBookingForm
from ..models import db, Booking, User

bp = Blueprint('bookings', __name__, url_prefix='/bookings')
logger = setup_logger(__name__, 'bookings.log')


@bp.record_once
def register_errors(state) -> None:
    @state.app.errorhandler(ValueError)
    def handle_conflict(err: ValueError):
        if request.blueprint == 'api_v1':
            return jsonify(error=str(err)), 409
        flash(str(err))
        return redirect(request.url)


@bp.route('/board')
@login_required
def reservation_board() -> str:
    """Display all bookings."""
    bookings = db.session.query(Booking).all()
    form = SearchBookingForm()
    return render_template('board.html', bookings=bookings, search_form=form)


@bp.route('/available')
@login_required
def available_rooms():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify([])
    rooms = RoomService.available_rooms(date.fromisoformat(start), date.fromisoformat(end))
    return jsonify([{'id': r.id, 'number': r.number} for r in rooms])


@bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
def new_booking():
    """Create a booking."""
    form = BookingForm()
    form.user_id.choices = [(u.id, u.username) for u in AuthService.list_users()]
    if form.start_date.data and form.end_date.data:
        avail = RoomService.available_rooms(form.start_date.data, form.end_date.data)
    else:
        avail = RoomService.list_rooms()
    form.room_id.choices = [(r.id, r.number) for r in avail]
    if form.validate_on_submit():
        try:
            BookingService.create_booking(
                form.user_id.data,
                form.room_id.data,
                form.start_date.data,
                form.end_date.data,
            )
            return redirect(url_for('bookings.reservation_board'))
        except ValueError as exc:
            form.start_date.errors.append(str(exc))
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


@bp.route('/cancel/<int:bid>', methods=['POST'])
@login_required
def cancel_booking(bid: int):
    BookingService.cancel_booking(bid)
    return redirect(url_for('bookings.reservation_board'))


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('receptionist')
def edit_booking(id: int):
    """Edit an existing booking."""
    booking = db.session.get(Booking, id)
    if not booking:
        return redirect(url_for('bookings.reservation_board'))
    form = EditBookingForm(
        guest_name=booking.user.username if booking.user else '',
        start_date=booking.start_date,
        end_date=booking.end_date,
    )
    if form.validate_on_submit():
        BookingService.update_booking(
            id,
            guest_name=form.guest_name.data,
            check_in=form.start_date.data,
            check_out=form.end_date.data,
        )
        return redirect(url_for('bookings.reservation_board'))
    return render_template('edit_booking.html', form=form, booking=booking)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('receptionist')
def delete_booking(id: int):
    """Delete a booking."""
    BookingService.delete_booking(id)
    return redirect(url_for('bookings.reservation_board'))


@bp.route('/calendar')
@login_required
def calendar_view():
    bookings = BookingService.list_bookings()
    return render_template('calendar.html', bookings=bookings)


@bp.route('/guest/<int:uid>')
@login_required
def guest_profile(uid: int):
    user = db.session.get(User, uid)
    bookings = Booking.query.filter_by(user_id=uid).all()
    return render_template('guest_profile.html', user=user, bookings=bookings)


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """Search bookings by guest or date range."""
    form = SearchBookingForm()
    bookings = []
    if form.validate_on_submit():
        bookings = BookingService.search_bookings(
            query=form.guest_name.data,
            start=form.start_date.data,
            end=form.end_date.data,
        )
    return render_template('board.html', bookings=bookings, search_form=form)

