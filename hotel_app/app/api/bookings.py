# PLAN: REST endpoints for Booking resource with API key auth.
from __future__ import annotations

from datetime import date
from flask import jsonify, url_for
from werkzeug.exceptions import NotFound, BadRequest

from . import api_bp
from .schemas import to_dict, require_json
from ..services.booking_service import BookingService
from ..models import db, Booking


def _parse_date(val: str) -> date:
    try:
        return date.fromisoformat(val)
    except ValueError as exc:
        raise BadRequest('invalid date') from exc


@api_bp.route('/bookings/', methods=['GET'])
def list_bookings_api():
    """Return all bookings."""
    bookings = BookingService.list_bookings()
    return jsonify([to_dict(b) for b in bookings])


@api_bp.route('/bookings/<int:bid>', methods=['GET'])
def get_booking(bid: int):
    """Retrieve one booking."""
    booking = db.session.get(Booking, bid)
    if not booking:
        raise NotFound()
    return jsonify(to_dict(booking))


@api_bp.route('/bookings/', methods=['POST'])
def create_booking_api():
    """Create a booking and return 201."""
    data = require_json('user_id', 'room_id', 'start_date', 'end_date')
    booking = BookingService.create_booking(
        data['user_id'],
        data['room_id'],
        _parse_date(data['start_date']),
        _parse_date(data['end_date']),
    )
    resp = jsonify(to_dict(booking))
    resp.status_code = 201
    resp.headers['Location'] = url_for('api_v1.get_booking', bid=booking.id)
    return resp


@api_bp.route('/bookings/<int:bid>', methods=['PATCH'])
def update_booking_api(bid: int):
    """Patch booking fields."""
    booking = db.session.get(Booking, bid)
    if not booking:
        raise NotFound()
    data = require_json()
    BookingService.update_booking(
        bid,
        guest_name=data.get('guest_name'),
        check_in=_parse_date(data['check_in']) if 'check_in' in data else None,
        check_out=_parse_date(data['check_out']) if 'check_out' in data else None,
    )
    booking = db.session.get(Booking, bid)
    return jsonify(to_dict(booking))


@api_bp.route('/bookings/<int:bid>', methods=['DELETE'])
def delete_booking_api(bid: int):
    """Delete booking."""
    BookingService.delete_booking(bid)
    return '', 204

