from __future__ import annotations

from typing import List

from ..models import CleaningLog, db


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
