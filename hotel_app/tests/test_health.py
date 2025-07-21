import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from config import TestingConfig


def test_health_route():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
    client = app.test_client()
    resp = client.get('/health')
    assert resp.json == {'status': 'ok'}
