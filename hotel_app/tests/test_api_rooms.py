# PLAN: Verify room API auth and listing/creation behaviour.
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.room_service import RoomService


def make_client():
    app = create_app('config.TestingConfig')
    app.config['API_KEY'] = 'secret'
    with app.app_context():
        db.create_all()
        RoomService.create_room('101', 'std')
    return app.test_client(), app


def test_rooms_auth_required():
    client, _ = make_client()
    res = client.get('/api/v1/rooms/')
    assert res.status_code == 401


def test_rooms_list_create():
    client, app = make_client()
    hdr = {'X-API-Key': 'secret'}
    res = client.get('/api/v1/rooms/', headers=hdr)
    assert res.status_code == 200
    assert len(res.get_json()) == 1
    res = client.post('/api/v1/rooms/', json={'number': '102', 'status': 'vacant'}, headers=hdr)
    assert res.status_code == 201
    with app.app_context():
        assert len(RoomService.list_rooms()) == 2

