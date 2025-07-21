from __future__ import annotations

import logging

from flask import Blueprint, render_template

from ..services.housekeeping_service import HousekeepingService
from ..utils import login_required, role_required, setup_logger
from ..models import db, HousekeepingTask

bp = Blueprint('housekeeping', __name__, url_prefix='/housekeeping')
logger = setup_logger(__name__, 'housekeeping.log')


@bp.route('/tasks')
@login_required
def tasks() -> str:
    """Display all housekeeping tasks."""
    tasks = db.session.query(HousekeepingTask).all()
    return render_template('tasks.html', tasks=tasks)


@bp.route('/tasks/<int:id>/complete', methods=['POST'])
@login_required
@role_required('housekeeping')
def complete_task(id: int):
    """Mark a task as completed."""
    HousekeepingService.complete_task(id)
    return redirect(url_for('housekeeping.tasks'))

