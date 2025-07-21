import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


def test_overlap_rejected():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('u', 'p', 'manager')
        room = RoomService.create_room('1', 'std')
        BookingService.create_booking(user.id, room.id, date(2030, 1, 1), date(2030, 1, 2))
        try:
            BookingService.create_booking(user.id, room.id, date(2030, 1, 1), date(2030, 1, 3))
            assert False, 'expected error'
        except ValueError:
            assert True


def test_state_transitions():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('u2', 'p', 'manager')
        room = RoomService.create_room('2', 'std')
        booking = BookingService.create_booking(user.id, room.id, date.today(), date.today())
        BookingService.check_in(booking.id)
        assert db.session.get(type(booking), booking.id).status == 'checked-in'
        BookingService.check_out(booking.id)
        assert db.session.get(type(booking), booking.id).status == 'cancelled'
