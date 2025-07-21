from __future__ import annotations

from datetime import date

from ..models import Booking, db


class BookingService:
    """Service for managing bookings."""

    @staticmethod
    def create_booking(user_id: int, room_id: int, start: date, end: date) -> Booking:
        booking = Booking(user_id=user_id, room_id=room_id, start_date=start, end_date=end)
        db.session.add(booking)
        db.session.commit()
        return booking
