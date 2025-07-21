# PLAN: room CRUD helpers for views; update and delete operations.
from __future__ import annotations

from typing import List

from ..models import Room, db


class RoomService:
    """Service handling room CRUD operations."""

    @staticmethod
    def create_room(number: str, type: str) -> Room:
        room = Room(number=number, type=type)
        db.session.add(room)
        db.session.commit()
        return room

    @staticmethod
    def list_rooms() -> List[Room]:
        return Room.query.all()

    @staticmethod
    def update_room(room_id: int, number: str | None = None, status: str | None = None) -> Room | None:
        """Update room fields if found."""
        room = db.session.get(Room, room_id)
        if not room:
            return None
        if number is not None:
            room.number = number
        if status is not None:
            room.status = status
        db.session.commit()
        return room

    @staticmethod
    def delete_room(room_id: int) -> None:
        """Delete a room by id."""
        room = db.session.get(Room, room_id)
        if room:
            db.session.delete(room)
            db.session.commit()
