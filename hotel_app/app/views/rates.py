# PLAN: CRUD for rate strategies with activation toggle
from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for, request

from ..models import RatePlan, RateStrategy, BARRate, PackageRate, CorporateRate, db
from ..utils import login_required, role_required

bp = Blueprint('rates', __name__, url_prefix='/rates')


@bp.route('/')
@login_required
@role_required('manager')
def list_rates():
    plans = RatePlan.query.all()
    return render_template('rates.html', plans=plans)


@bp.route('/toggle/<int:rid>')
@login_required
@role_required('manager')
def toggle_rate(rid: int):
    strat = db.session.get(RateStrategy, rid)
    if strat:
        strat.active = not strat.active
        db.session.commit()
    return redirect(url_for('rates.list_rates'))
