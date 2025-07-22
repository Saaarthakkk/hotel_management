# PLAN: compute daily metrics and export to CSV/PDF with Chart.js data
from __future__ import annotations

from datetime import date, timedelta
from statistics import mean
import pandas as pd
from weasyprint import HTML

from ..models import Room, Booking, HousekeepingTask, RatePlan, db


class AnalyticsService:
    """Service computing occupancy and revenue metrics."""

    @staticmethod
    def daily_metrics(start: date, end: date) -> list[dict]:
        rows = []
        d = start
        while d <= end:
            occ = (
                Booking.query.filter(
                    Booking.start_date <= d,
                    Booking.end_date >= d,
                    Booking.status != 'cancelled',
                ).count()
            )
            total = Room.query.count()
            occupancy = occ / total if total else 0
            rates = []
            for b in Booking.query.filter(
                Booking.start_date <= d,
                Booking.end_date >= d,
            ).all():
                plan = RatePlan.query.filter_by(room_type=b.room.type).first()
                if plan:
                    rates.append(plan.dynamic_rate)
            adr = mean(rates) if rates else 0.0
            revpar = adr * occupancy
            load = HousekeepingTask.query.filter_by(due_date=d).count()
            rows.append(
                {
                    'date': d.isoformat(),
                    'occupancy': occupancy,
                    'adr': adr,
                    'revpar': revpar,
                    'load': load,
                }
            )
            d += timedelta(days=1)
        return rows

    @staticmethod
    def to_csv(rows: list[dict], path: str) -> str:
        """Write metrics to CSV file. HL: file I/O."""
        pd.DataFrame(rows).to_csv(path, index=False)
        return path

    @staticmethod
    def to_pdf(html: str, path: str) -> str:
        """Render HTML to PDF using WeasyPrint."""
        HTML(string=html).write_pdf(path)
        return path
