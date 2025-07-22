import os, sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService
from app.services import forecast_service


def test_forecast_stub(monkeypatch):
    monkeypatch.setattr(forecast_service, 'Prophet', None)
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('u', 'p', 'manager')
        r = RoomService.create_room('1', 'std')
        BookingService.create_booking(user.id, r.id, date.today(), date.today())
        rows = forecast_service.ForecastService.forecast()
        assert len(rows) == 30
        assert rows[0][1] >= 0
