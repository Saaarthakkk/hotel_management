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

    @staticmethod
    def list_bookings() -> list[Booking]:
        return Booking.query.all()

    @staticmethod
    def check_in(booking_id: int) -> None:
        booking = Booking.query.get(booking_id)
        if booking:
            booking.is_checked_in = True
            db.session.commit()

    @staticmethod
    def check_out(booking_id: int) -> None:
        booking = Booking.query.get(booking_id)
        if booking:
            booking.is_checked_in = False
            db.session.commit()
