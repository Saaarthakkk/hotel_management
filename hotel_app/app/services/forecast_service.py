# PLAN: train or mock forecast model and write forecast.csv
from __future__ import annotations

from datetime import date, timedelta
from typing import List, Tuple

import pandas as pd

try:
    from prophet import Prophet  # type: ignore
except Exception:  # pragma: no cover - offline fallback
    Prophet = None

from ..models import Booking


class ForecastService:
    """Predict booking demand for the next 30 days."""

    @staticmethod
    def _recursive_avg(arr: List[int], idx: int) -> float:
        """HL: recursion to compute mean."""
        if idx == 0:
            return arr[0]
        return (arr[idx] + idx * ForecastService._recursive_avg(arr, idx - 1)) / (
            idx + 1
        )

    @staticmethod
    def forecast() -> List[Tuple[date, int]]:
        bookings = [b.start_date for b in Booking.query.all()]
        df = pd.DataFrame({'ds': bookings, 'y': 1}).groupby('ds').sum().reset_index()
        if Prophet:
            m = Prophet(daily_seasonality=True)
            m.fit(df)
            future = m.make_future_dataframe(periods=30)
            fc = m.predict(future).tail(30)
            rows = [(r['ds'].date(), int(r['yhat'])) for r in fc.to_dict('records')]
        else:
            counts = df['y'].tolist() or [1]
            avg = ForecastService._recursive_avg(counts, len(counts) - 1)
            last = df['ds'].max() if not df.empty else date.today()
            rows = []
            for i in range(1, 31):
                last += timedelta(days=1)
                rows.append((last, int(avg)))
        pd.DataFrame(rows, columns=['date', 'demand']).to_csv('forecast.csv', index=False)
        return rows
