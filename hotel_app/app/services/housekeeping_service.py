# PLAN: create, assign and complete housekeeping tasks with validation
from __future__ import annotations

from datetime import datetime, date
from typing import List

from ..models import CleaningLog, HousekeepingTask, User, db


class HousekeepingService:
    """Service to log room cleanings."""

    @staticmethod
    def log_cleaning(task_id: int, duration: int) -> CleaningLog:
        """Record cleaning duration for a task."""
        log = CleaningLog(task_id=task_id, duration=duration)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def list_logs() -> List[CleaningLog]:
        return CleaningLog.query.all()

    @staticmethod
    def schedule_task(room_id: int, due_date: date, priority: int = 1) -> HousekeepingTask:
        if due_date < date.today():
            raise ValueError('due_date cannot be past')  # HL: data validation
        task = HousekeepingTask(room_id=room_id, due_date=due_date, priority=priority)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def assign_task(task_id: int, user_id: int) -> None:
        task = db.session.get(HousekeepingTask, task_id)
        if task:
            task.assigned_to = user_id
            task.status = 'assigned'
            db.session.commit()

    @staticmethod
    def complete_task(task_id: int) -> None:
        """Mark a housekeeping task as done."""
        task = db.session.get(HousekeepingTask, task_id)
        if task:
            task.status = 'done'
            task.completed_at = datetime.utcnow()
            db.session.commit()

    @staticmethod
    def list_tasks() -> List[HousekeepingTask]:
        return HousekeepingTask.query.all()

    @staticmethod
    def tasks_for_user(uid: int) -> List[HousekeepingTask]:
        return HousekeepingTask.query.filter_by(assigned_to=uid, completed_at=None).all()

    @staticmethod
    def list_unassigned() -> List[HousekeepingTask]:
        return HousekeepingTask.query.filter_by(assigned_to=None, completed_at=None).all()

    @staticmethod
    def housekeeping_users() -> List[User]:
        return User.query.filter_by(role='housekeeping').all()
