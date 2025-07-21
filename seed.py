from app import create_app
from app.models import db
from app.services.auth_service import AuthService


def seed() -> None:
    app = create_app('config.DevelopmentConfig')
    with app.app_context():
        db.create_all()
        roles = ['admin', 'manager', 'receptionist', 'housekeeping']
        for role in roles:
            username = f'{role}_demo'
            if not AuthService.authenticate(username, 'pass123'):
                AuthService.create_user(username, 'pass123', role)


if __name__ == '__main__':
    seed()
