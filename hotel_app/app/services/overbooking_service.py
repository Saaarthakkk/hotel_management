# PLAN: Monte Carlo simulation to compute oversell limit
from __future__ import annotations

from datetime import date
from typing import List
import numpy as np

from ..models import Booking, Room, OverbookingPlan, db


class OverbookingService:
    """Estimate oversell limits via simulation."""

    @staticmethod
    def compute_limit(target: date, trials: int = 500) -> int:
        noshows = [b for b in Booking.query.filter(Booking.end_date < target)]
        rate = (
            sum(1 for b in noshows if b.status == 'reserved') / len(noshows)
            if noshows
            else 0.1
        )
        rooms = Room.query.count()
        results: List[int] = []
        for _ in range(trials):  # HL: nested loops + 2-D arrays
            arrivals = np.random.poisson(rooms)
            stay = 0
            for _ in range(arrivals):
                if np.random.rand() >= rate:
                    stay += 1
            results.append(stay - rooms)
        limit = max(0, int(np.mean(results)))
        return limit

    @staticmethod
    def record_plan(target: date, limit: int) -> OverbookingPlan:
        plan = OverbookingPlan(date=target, limit=limit)
        db.session.add(plan)
        db.session.commit()
        return plan
