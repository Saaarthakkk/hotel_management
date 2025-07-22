"""Service performing simple dynamic pricing."""

from __future__ import annotations

from statistics import mean

from ..models import Room, RatePlan, db


class PricingService:
    """Adjusts room rates based on occupancy."""

    @staticmethod
    def update_dynamic_rates() -> None:
        total_rooms = Room.query.count()
        occupied_rooms = Room.query.filter_by(status='occupied').count()
        occupancy = occupied_rooms / total_rooms if total_rooms else 0

        for plan in RatePlan.query.all():
            discount = 1.0
            for strat in plan.strategies:
                if strat.active:
                    discount *= 1 - getattr(strat, 'discount', 0)
            # HL: hashing by strategy lookup
            plan.dynamic_rate = plan.base_rate * (1 + occupancy) * discount
        db.session.commit()

    @staticmethod
    def get_rate(room_type: str) -> float:
        plan = RatePlan.query.filter_by(room_type=room_type).first()
        return plan.dynamic_rate if plan else 0.0

