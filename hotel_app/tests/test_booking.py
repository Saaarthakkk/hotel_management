import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from config import TestingConfig
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


def test_check_in_and_out():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('u1', 'pass', 'manager')
        room = RoomService.create_room('101', 'std')
        booking = BookingService.create_booking(user.id, room.id, date.today(), date.today())
        BookingService.check_in(booking.id)
        assert BookingService.list_bookings()[0].is_checked_in is True
        assert RoomService.list_rooms()[0].status == 'occupied'
        BookingService.check_out(booking.id)
        assert BookingService.list_bookings()[0].is_checked_in is False
        assert RoomService.list_rooms()[0].status == 'vacant'
