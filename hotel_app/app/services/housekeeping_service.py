from __future__ import annotations

from typing import List

from ..models import CleaningLog, HousekeepingTask, db


class HousekeepingService:
    """Service to log room cleanings."""

    @staticmethod
    def log_cleaning(room_id: int, notes: str = '') -> CleaningLog:
        log = CleaningLog(room_id=room_id, notes=notes)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def list_logs() -> List[CleaningLog]:
        return CleaningLog.query.all()

    @staticmethod
    def schedule_task(room_id: int, due_date) -> HousekeepingTask:
        task = HousekeepingTask(room_id=room_id, due_date=due_date)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def complete_task(task_id: int) -> None:
        task = db.session.get(HousekeepingTask, task_id)
        if task:
            task.status = 'done'
            db.session.commit()

    @staticmethod
    def list_tasks() -> List[HousekeepingTask]:
        return HousekeepingTask.query.all()
