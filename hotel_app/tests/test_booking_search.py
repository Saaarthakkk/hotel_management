import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


def test_booking_search():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user1 = AuthService.create_user('Alice', 'p', 'manager')
        user2 = AuthService.create_user('Bob', 'p', 'manager')
        room = RoomService.create_room('1', 'std')
        BookingService.create_booking(user1.id, room.id, date(2025,1,1), date(2025,1,2))
        BookingService.create_booking(user2.id, room.id, date(2025,2,1), date(2025,2,2))
        res = BookingService.search_bookings(query='Ali')
        assert len(res) == 1
        res = BookingService.search_bookings(start=date(2025,2,1), end=date(2025,2,2))
        assert len(res) == 1


