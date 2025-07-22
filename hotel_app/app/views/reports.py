# PLAN: manager dashboard providing metrics and forecast JSON
from __future__ import annotations

from datetime import date
from flask import Blueprint, render_template, jsonify, request

from ..services.analytics_service import AnalyticsService
from ..services.forecast_service import ForecastService
from ..services.overbooking_service import OverbookingService
from ..models import OverbookingPlan
from ..utils import login_required, role_required

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/overview.json')
@login_required
@role_required('manager')
def overview_json():
    today = date.today()
    metrics = AnalyticsService.daily_metrics(today, today)
    forecast = ForecastService.forecast()
    plan = OverbookingPlan.query.filter_by(date=today).first()
    limit = plan.limit if plan else None
    return jsonify({'metrics': metrics, 'forecast': forecast, 'oversell': limit})


@bp.route('/ui')
@login_required
@role_required('manager')
def dashboard():
    return render_template('reports.html')
