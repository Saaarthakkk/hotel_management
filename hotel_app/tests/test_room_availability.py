import os, sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


def test_available_rooms():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('u','p','manager')
        r1 = RoomService.create_room('1','std')
        r2 = RoomService.create_room('2','std')
        BookingService.create_booking(user.id, r1.id, date(2030,1,1), date(2030,1,3))
        avail = RoomService.available_rooms(date(2030,1,1), date(2030,1,3))
        assert r2 in avail and r1 not in avail
