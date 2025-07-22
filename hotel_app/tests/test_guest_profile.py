import os, sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


def test_guest_profile_view():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    with app.app_context():
        db.create_all()
        guest = AuthService.create_user('guest','p','manager')
        gid = guest.id
        room = RoomService.create_room('1','std')
        BookingService.create_booking(guest.id, room.id, date.today(), date.today())
    with client.session_transaction() as sess:
        sess['user_id'] = gid
        sess['role'] = 'manager'
    resp = client.get(f'/bookings/guest/{gid}')
    assert resp.status_code == 200
    assert b'Bookings' in resp.data
