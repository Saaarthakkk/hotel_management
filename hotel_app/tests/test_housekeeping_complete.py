import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.room_service import RoomService
from app.services.housekeeping_service import HousekeepingService


def test_complete_task():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        room = RoomService.create_room('1', 'std')
        task = HousekeepingService.schedule_task(room.id, date.today())
        HousekeepingService.complete_task(task.id)
        assert HousekeepingService.list_tasks()[0].status == 'done'


