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
