# PLAN: Test booking API endpoints.
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


def make_client():
    app = create_app('config.TestingConfig')
    app.config['API_KEY'] = 'secret'
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('guest', 'p', 'manager')
        room = RoomService.create_room('201', 'std')
        BookingService.create_booking(user.id, room.id, date.today(), date.today())
    return app.test_client(), app


def test_bookings_auth_required():
    client, _ = make_client()
    assert client.get('/api/v1/bookings/').status_code == 401


def test_bookings_list_and_create():
    client, app = make_client()
    hdr = {'X-API-Key': 'secret'}
    res = client.get('/api/v1/bookings/', headers=hdr)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    res = client.post(
        '/api/v1/bookings/',
        json={'user_id': 1, 'room_id': 1, 'start_date': '2030-01-01', 'end_date': '2030-01-02'},
        headers=hdr,
    )
    assert res.status_code == 201
    with app.app_context():
        assert len(BookingService.list_bookings()) == 2

