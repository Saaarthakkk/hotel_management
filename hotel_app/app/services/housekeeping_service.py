# PLAN: create, assign and complete housekeeping tasks with validation
from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import List

from ..models import CleaningLog, HousekeepingTask, User, db


class HousekeepingService:
    """Service to log room cleanings."""

    @staticmethod
    def log_cleaning(task_id: int, duration: int, booking_id: int | None = None) -> CleaningLog:
        """Record cleaning duration for a task."""
        log = CleaningLog(task_id=task_id, booking_id=booking_id, duration=duration)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def list_logs() -> List[CleaningLog]:
        return CleaningLog.query.all()

    @staticmethod
    def schedule_task(
        room_id: int,
        due_date: date,
        priority: int = 1,
        booking_id: int | None = None,
        recurrence_days: int | None = None,
    ) -> HousekeepingTask:
        if due_date < date.today():
            raise ValueError('due_date cannot be past')  # HL: data validation
        task = HousekeepingTask(
            room_id=room_id,
            due_date=due_date,
            priority=priority,
            booking_id=booking_id,
            recurrence_days=recurrence_days,
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def schedule_recurring_task(
        room_id: int,
        start_date: date,
        end_date: date,
        interval_days: int,
        priority: int = 1,
    ) -> List[HousekeepingTask]:
        """Create multiple tasks in a sequence."""
        tasks: List[HousekeepingTask] = []
        current = start_date
        while current <= end_date:  # HL: nested loops
            tasks.append(
                HousekeepingService.schedule_task(
                    room_id,
                    current,
                    priority,
                    recurrence_days=interval_days,
                )
            )
            current += timedelta(days=interval_days)
        return tasks

    @staticmethod
    def assign_task(task_id: int, user_id: int) -> None:
        task = db.session.get(HousekeepingTask, task_id)
        if task:
            task.assigned_to = user_id
            task.status = 'assigned'
            db.session.commit()

    @staticmethod
    def complete_task(task_id: int, duration: int = 0) -> None:
        """Mark a housekeeping task as done."""
        task = db.session.get(HousekeepingTask, task_id)
        if task:
            task.status = 'done'
            task.completed_at = datetime.utcnow()
            HousekeepingService.log_cleaning(task_id, duration, task.booking_id)
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
