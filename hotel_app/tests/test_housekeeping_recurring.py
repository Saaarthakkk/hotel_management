import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.housekeeping_service import HousekeepingService
from app.services.booking_service import BookingService


def test_schedule_recurring():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        room = RoomService.create_room('10', 'std')
        tasks = HousekeepingService.schedule_recurring_task(
            room.id, date.today(), date.today() + timedelta(days=2), 1
        )
        assert len(tasks) == 3


def test_booking_cleaning_log():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('hkmanager', 'p', 'manager')
        room = RoomService.create_room('20', 'std')
        booking = BookingService.create_booking(user.id, room.id, date.today(), date.today())
        BookingService.check_in(booking.id)
        BookingService.check_out(booking.id)
        task = HousekeepingService.list_unassigned()[0]
        HousekeepingService.complete_task(task.id, duration=15)
        log = HousekeepingService.list_logs()[0]
        assert log.booking_id == booking.id
