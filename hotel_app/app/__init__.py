from __future__ import annotations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .models import db

csrf = CSRFProtect()
migrate = Migrate()


def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .views import auth_bp, rooms_bp, bookings_bp, housekeeping_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(housekeeping_bp)

    @app.route('/health')
    def health():
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return {'status': 'ok'}

    return app
