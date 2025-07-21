from __future__ import annotations

import logging

# PLAN: show assigned/unassigned tasks with assign and complete actions
from flask import Blueprint, render_template, redirect, url_for, session, flash

from ..services.housekeeping_service import HousekeepingService
from ..utils import login_required, role_required, setup_logger
from ..models import db, HousekeepingTask, User
from .. import cli

bp = Blueprint('housekeeping', __name__, url_prefix='/housekeeping')
logger = setup_logger(__name__, 'housekeeping.log')


@bp.record_once
def init_cli(state) -> None:
    cli.init_cli(state.app)


@bp.route('/tasks')
@login_required
def tasks() -> str:
    """Display tasks for the current user and unassigned ones."""
    my_tasks = HousekeepingService.tasks_for_user(session.get('user_id'))
    unassigned = HousekeepingService.list_unassigned()
    users = HousekeepingService.housekeeping_users()
    return render_template(
        'tasks.html',
        my_tasks=my_tasks,
        unassigned=unassigned,
        users=users,
        role=session.get('role'),
    )


@bp.route('/tasks/<int:id>/complete', methods=['POST'])
@login_required
@role_required('housekeeping')
def complete_task(id: int):
    """Mark a task as completed."""
    HousekeepingService.complete_task(id)
    flash('Task completed')
    return redirect(url_for('housekeeping.tasks'))


@bp.route('/tasks/<int:id>/assign/<int:user_id>', methods=['POST'])
@login_required
@role_required('manager')
def assign_task(id: int, user_id: int):
    """Assign a task to a user."""
    HousekeepingService.assign_task(id, user_id)
    flash('Task assigned')
    return redirect(url_for('housekeeping.tasks'))

