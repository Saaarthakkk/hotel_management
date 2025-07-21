# PLAN: Test housekeeping API routes.
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.room_service import RoomService
from app.services.housekeeping_service import HousekeepingService


def make_client():
    app = create_app('config.TestingConfig')
    app.config['API_KEY'] = 'secret'
    with app.app_context():
        db.create_all()
        room = RoomService.create_room('301', 'std')
        HousekeepingService.schedule_task(room.id, date.today())
    return app.test_client(), app


def test_tasks_auth():
    client, _ = make_client()
    assert client.get('/api/v1/tasks/').status_code == 401


def test_tasks_list_and_complete():
    client, app = make_client()
    hdr = {'X-API-Key': 'secret'}
    res = client.get('/api/v1/tasks/', headers=hdr)
    assert res.status_code == 200
    tid = res.get_json()[0]['id']
    res = client.patch(f'/api/v1/tasks/{tid}', json={'completed': True}, headers=hdr)
    assert res.status_code == 200
    with app.app_context():
        assert HousekeepingService.list_tasks()[0].status == 'done'

