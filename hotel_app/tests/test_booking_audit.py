import os, sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService
from app.models import BookingAudit


def test_cancel_creates_audit():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        user = AuthService.create_user('u','p','manager')
        room = RoomService.create_room('1','std')
        b = BookingService.create_booking(user.id, room.id, date.today(), date.today())
        BookingService.cancel_booking(b.id)
        audits = BookingAudit.query.filter_by(booking_id=b.id, action='cancel').all()
        assert len(audits) == 1
        assert b.status == 'cancelled'
