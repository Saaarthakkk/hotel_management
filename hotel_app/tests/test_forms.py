import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from config import TestingConfig
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


def test_room_form_route():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('admin', 'p', 'manager')
        with client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['role'] = 'manager'
        resp = client.get('/rooms/new')
        assert resp.status_code == 200
        resp = client.post('/rooms/new', data={'number': '201', 'type': 'suite'}, follow_redirects=True)
        assert resp.status_code == 200
        assert any(r.number == '201' for r in RoomService.list_rooms())


def test_booking_form_route():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    with app.app_context():
        db.create_all()
        receptionist = AuthService.create_user('rec', 'p', 'receptionist')
        guest = AuthService.create_user('guest', 'p', 'manager')
        room = RoomService.create_room('301', 'std')
        with client.session_transaction() as sess:
            sess['user_id'] = receptionist.id
            sess['role'] = 'receptionist'
        resp = client.get('/bookings/new')
        assert resp.status_code == 200
        resp = client.post(
            '/bookings/new',
            data={
                'user_id': guest.id,
                'room_id': room.id,
                'start_date': '2025-01-01',
                'end_date': '2025-01-02',
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert len(BookingService.list_bookings()) == 1
