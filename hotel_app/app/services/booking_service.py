# PLAN: manage booking lifecycle including update, delete, and search helpers.
from __future__ import annotations

from datetime import date, datetime

from ..models import Booking, BookingAudit, User, db


class BookingService:
    """Service for managing bookings."""

    @staticmethod
    def create_booking(user_id: int, room_id: int, start: date, end: date) -> Booking:
        overlap = (
            db.session.query(Booking)
            .filter(Booking.room_id == room_id, Booking.status != 'cancelled')
            .filter(Booking.end_date >= start, Booking.start_date <= end)
            .first()
        )
        if overlap:
            raise ValueError('Room already booked for given dates')
        booking = Booking(user_id=user_id, room_id=room_id, start_date=start, end_date=end)
        db.session.add(booking)
        db.session.commit()
        BookingService._record_audit(booking.id, 'create')
        return booking

    @staticmethod
    def list_bookings() -> list[Booking]:
        return Booking.query.all()

    @staticmethod
    def check_in(booking_id: int) -> None:
        """Mark booking as checked in and update room status."""
        booking = db.session.get(Booking, booking_id)
        if booking and booking.status == 'reserved':
            booking.status = 'checked-in'
            if booking.room:
                booking.room.status = 'occupied'
            db.session.commit()
            BookingService._record_audit(booking.id, 'check_in')

    @staticmethod
    def check_out(booking_id: int) -> None:
        """Mark booking as checked out and free the room."""
        booking = db.session.get(Booking, booking_id)
        if booking and booking.status == 'checked-in':
            booking.status = 'cancelled'
            booking.cancelled_at = datetime.utcnow()
            if booking.room:
                booking.room.status = 'vacant'
            db.session.commit()
            BookingService._record_audit(booking.id, 'check_out')

    @staticmethod
    def update_booking(
        booking_id: int,
        guest_name: str | None = None,
        check_in: date | None = None,
        check_out: date | None = None,
        status: str | None = None,
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
        if status is not None:
            booking.status = status
        db.session.commit()
        BookingService._record_audit(booking.id, 'update')
        return booking

    @staticmethod
    def delete_booking(booking_id: int) -> None:
        """Delete a booking."""
        booking = db.session.get(Booking, booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            BookingService._record_audit(booking_id, 'delete')

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

    @staticmethod
    def cancel_booking(booking_id: int) -> None:
        booking = db.session.get(Booking, booking_id)
        if booking and booking.status != 'cancelled':
            booking.status = 'cancelled'
            booking.cancelled_at = datetime.utcnow()
            if booking.room:
                booking.room.status = 'vacant'
            db.session.commit()
            BookingService._record_audit(booking.id, 'cancel')

    @staticmethod
    def _record_audit(bid: int, action: str, details: str | None = None) -> None:
        audit = BookingAudit(booking_id=bid, action=action, details=details or '')
        db.session.add(audit)
        db.session.commit()
