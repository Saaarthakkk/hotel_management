import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.room_service import RoomService


def test_room_crud():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        room = RoomService.create_room('1', 'std')
        RoomService.update_room(room.id, number='2', status='vacant')
        updated = RoomService.list_rooms()[0]
        assert updated.number == '2'
        RoomService.delete_room(room.id)
        assert RoomService.list_rooms() == []


