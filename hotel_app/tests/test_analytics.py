import os, sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService
from app.services.analytics_service import AnalyticsService


def test_occupancy_csv(tmp_path):
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('u', 'p', 'manager')
        r1 = RoomService.create_room('1', 'std')
        r2 = RoomService.create_room('2', 'std')
        BookingService.create_booking(user.id, r1.id, date.today(), date.today())
        rows = AnalyticsService.daily_metrics(date.today(), date.today())
        assert abs(rows[0]['occupancy'] - 0.5) < 0.01
        path = AnalyticsService.to_csv(rows, tmp_path/'m.csv')
        assert os.path.exists(path)
