# PLAN: manage booking lifecycle including update, delete, and search helpers.
from __future__ import annotations

from datetime import date

from ..models import Booking, User, db


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
        """Mark booking as checked in and update room status."""
        booking = db.session.get(Booking, booking_id)
        if booking:
            booking.is_checked_in = True
            if booking.room:
                booking.room.status = 'occupied'
            db.session.commit()

    @staticmethod
    def check_out(booking_id: int) -> None:
        """Mark booking as checked out and free the room."""
        booking = db.session.get(Booking, booking_id)
        if booking:
            booking.is_checked_in = False
            if booking.room:
                booking.room.status = 'vacant'
            db.session.commit()

    @staticmethod
    def update_booking(
        booking_id: int,
        guest_name: str | None = None,
        check_in: date | None = None,
        check_out: date | None = None,
    ) -> Booking | None:
        """Update booking details and optionally guest name."""
        booking = db.session.get(Booking, booking_id)
        if not booking:
            return None
        if guest_name is not None and booking.user:
            booking.user.username = guest_name
        if check_in is not None:
            booking.start_date = check_in
        if check_out is not None:
            booking.end_date = check_out
        db.session.commit()
        return booking

    @staticmethod
    def delete_booking(booking_id: int) -> None:
        """Delete a booking."""
        booking = db.session.get(Booking, booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()

    @staticmethod
    def search_bookings(
        query: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> list[Booking]:
        """Return bookings filtered by guest name or date range."""
        q = Booking.query.join(User)
        if query:
            q = q.filter(User.username.ilike(f"%{query}%"))
        if start:
            q = q.filter(Booking.start_date >= start)
        if end:
            q = q.filter(Booking.end_date <= end)
        return q.all()
