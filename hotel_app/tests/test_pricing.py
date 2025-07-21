import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from config import TestingConfig
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService
from app.services.pricing_service import PricingService
from app.models import RatePlan


def test_dynamic_rate_increases_with_occupancy():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        plan = RatePlan(room_type='std', base_rate=100, dynamic_rate=100)
        db.session.add(plan)
        user = AuthService.create_user('u', 'p', 'manager')
        room1 = RoomService.create_room('1', 'std')
        room2 = RoomService.create_room('2', 'std')
        booking = BookingService.create_booking(user.id, room1.id, date.today(), date.today())
        BookingService.check_in(booking.id)
        PricingService.update_dynamic_rates()
        assert RatePlan.query.first().dynamic_rate > 100
