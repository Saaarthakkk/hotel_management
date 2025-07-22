import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db


def test_basic_routes():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['role'] = 'manager'
    assert client.get('/rooms/').status_code == 200
    assert client.get('/bookings/board').status_code == 200
    assert client.get('/housekeeping/tasks').status_code == 200

