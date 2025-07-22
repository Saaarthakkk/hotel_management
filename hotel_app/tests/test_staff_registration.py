import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from app.services.auth_service import AuthService


def test_staff_application_flow():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    with app.app_context():
        db.create_all()
    resp = client.post(
        '/auth/staff-register',
        data={
            'username': 'hk',
            'email': 'hk@example.com',
            'role': 'housekeeping',
            'password': 'StrongPass1',
            'confirm': 'StrongPass1',
            'agree': 'y',
        },
        follow_redirects=True,
    )
    assert b'pending manager approval' in resp.data
    with app.app_context():
        user = User.query.filter_by(username='hk').one()
        assert not user.active
        user.active = True
        db.session.commit()
    resp = client.post(
        '/auth/login',
        data={'email': 'hk@example.com', 'password': 'StrongPass1'},
        follow_redirects=True,
    )
    assert resp.status_code == 200

