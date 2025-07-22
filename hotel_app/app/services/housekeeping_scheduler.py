# PLAN: auto-assign tasks using min-heap priority queue and recursion helper
from __future__ import annotations

import heapq
from datetime import date
from typing import Dict, List

from .housekeeping_service import HousekeepingService
from ..models import HousekeepingTask, User, db


class HousekeepingScheduler:
    """Distribute tasks fairly using a priority queue (HL: queues)."""

    @staticmethod
    def generate_schedule(target: date) -> Dict[int, List[int]]:
        users = HousekeepingService.housekeeping_users()
        heap: list[tuple[int, int]] = []  # (load, user_id)
        schedule: dict[int, List[int]] = {}
        for u in users:
            heapq.heappush(heap, (0, u.id))
            schedule[u.id] = []
        tasks = (
            db.session.query(HousekeepingTask)
            .filter(
                HousekeepingTask.due_date == target,
                HousekeepingTask.completed_at.is_(None),
                HousekeepingTask.assigned_to.is_(None),
            )
            .order_by(HousekeepingTask.priority.desc())
            .all()
        )
        # HL: nested loops distributing tasks
        for t in tasks:
            load, uid = heapq.heappop(heap)
            schedule[uid].append(t.id)
            load += HousekeepingScheduler._roll_up_room_tasks(t)
            heapq.heappush(heap, (load, uid))
        return schedule

    @staticmethod
    def _roll_up_room_tasks(task: HousekeepingTask) -> int:
        """Recursively sum subtasks (HL: recursion)."""
        total = 1
        for sub in getattr(task, 'subtasks', []):
            total += HousekeepingScheduler._roll_up_room_tasks(sub)
        return total
