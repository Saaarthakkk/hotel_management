from __future__ import annotations

import logging

from flask import Blueprint, render_template, Response

from ..services.housekeeping_service import HousekeepingService
from ..utils import login_required, role_required, setup_logger

bp = Blueprint('housekeeping', __name__, url_prefix='/housekeeping')
logger = setup_logger(__name__, 'housekeeping.log')


@bp.route('/tasks')
@login_required
def tasks() -> Response:
    """Display all housekeeping tasks."""
    tasks = HousekeepingService.list_tasks()
    return render_template('tasks.html', tasks=tasks)
