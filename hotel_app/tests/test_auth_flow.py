import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from flask_login import current_user
import bcrypt


def test_registration_and_login():
    app = create_app('config.TestingConfig')
    client = app.test_client()
    with app.app_context():
        db.create_all()
        admin = AuthService.create_user('admin', 'pass', 'admin')
    # login as admin
    resp = client.post('/auth/login', data={'username': 'admin', 'password': 'pass'}, follow_redirects=True)
    assert resp.status_code == 200
    # register new user
    resp = client.post('/auth/register', data={'username': 'u1', 'password': 'pw', 'role': 'manager'}, follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        user = AuthService.authenticate('u1', 'pw')
        assert user is not None
        assert bcrypt.checkpw('pw'.encode(), user.password_hash.encode())


def test_password_hash():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('a', 'p', 'manager')
        assert user.password_hash != 'p'
        assert bcrypt.checkpw('p'.encode(), user.password_hash.encode())
