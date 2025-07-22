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
            email = f'{username}@example.com'
            if not AuthService.authenticate(email, 'pass123'):
                AuthService.create_user(username, 'pass123', role, email=email, active=True)


if __name__ == '__main__':
    seed()
