import os, sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.overbooking_service import OverbookingService
from app.services.room_service import RoomService


def test_overbooking_limit():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        RoomService.create_room('1', 'std')
        limit = OverbookingService.compute_limit(date.today(), trials=50)
        rooms = RoomService.list_rooms()
        assert 0 <= limit <= len(rooms)
