from __future__ import annotations

import logging
import os

from flask import Blueprint, render_template

from ..services.housekeeping_service import HousekeepingService
from ..utils import login_required, role_required

bp = Blueprint('housekeeping', __name__, url_prefix='/housekeeping')
logger = logging.getLogger(__name__)
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'housekeeping.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
handler = logging.FileHandler(log_path)
logger.addHandler(handler)


@bp.route('/tasks')
@login_required
def tasks():
    tasks = HousekeepingService.list_tasks()
    return render_template('tasks.html', tasks=tasks)
