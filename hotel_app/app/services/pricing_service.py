"""Service performing simple dynamic pricing."""

from __future__ import annotations

from statistics import mean

from ..models import Room, RatePlan, db


class PricingService:
    """Adjusts room rates based on occupancy."""

    @staticmethod
    def update_dynamic_rates() -> None:
        total_rooms = Room.query.count()
        booked_rooms = Room.query.filter_by(status='booked').count()
        occupancy = booked_rooms / total_rooms if total_rooms else 0

        for plan in RatePlan.query.all():
            plan.dynamic_rate = plan.base_rate * (1 + occupancy)
        db.session.commit()

    @staticmethod
    def get_rate(room_type: str) -> float:
        plan = RatePlan.query.filter_by(room_type=room_type).first()
        return plan.dynamic_rate if plan else 0.0

