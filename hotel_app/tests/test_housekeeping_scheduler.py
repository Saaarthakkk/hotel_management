import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.housekeeping_service import HousekeepingService
from app.services.housekeeping_scheduler import HousekeepingScheduler
from app.models import HousekeepingTask


def make_app():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        hk1 = AuthService.create_user('hk1', 'p', 'housekeeping')
        hk2 = AuthService.create_user('hk2', 'p', 'housekeeping')
        r1 = RoomService.create_room('1', 'std')
        r2 = RoomService.create_room('2', 'std')
        HousekeepingService.schedule_task(r1.id, date.today(), priority=2)
        HousekeepingService.schedule_task(r2.id, date.today(), priority=1)
    return app


def test_even_distribution():
    app = make_app()
    with app.app_context():
        sched = HousekeepingScheduler.generate_schedule(date.today())
        counts = [len(v) for v in sched.values()]
        assert max(counts) - min(counts) <= 1


def test_recursion_rollup():
    from app.services.housekeeping_scheduler import HousekeepingScheduler as HS

    class Node:
        def __init__(self, subs=None):
            self.subtasks = subs or []

    t = Node([Node(), Node([Node()])])
    assert HS._roll_up_room_tasks(t) == 4


def test_complete_route_sets_timestamp():
    app = make_app()
    client = app.test_client()
    with app.app_context():
        user = AuthService.authenticate('hk1', 'p')
        uid = user.id
        task = HousekeepingService.list_unassigned()[0]
        tid = task.id
        HousekeepingService.assign_task(tid, uid)
    with client.session_transaction() as sess:
        sess['user_id'] = uid
        sess['role'] = 'housekeeping'
    client.post(f'/housekeeping/tasks/{tid}/complete')
    with app.app_context():
        assert db.session.get(HousekeepingTask, tid).completed_at is not None
