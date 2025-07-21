# PLAN: REST endpoints for housekeeping tasks management.
from __future__ import annotations

from datetime import date
from flask import jsonify
from werkzeug.exceptions import NotFound, BadRequest

from . import api_bp
from .schemas import to_dict, require_json
from ..services.housekeeping_service import HousekeepingService
from ..models import db, HousekeepingTask


def _parse_date(val: str) -> date:
    try:
        return date.fromisoformat(val)
    except ValueError as exc:
        raise BadRequest('invalid date') from exc


@api_bp.route('/tasks/', methods=['GET'])
def list_tasks_api():
    """Return housekeeping tasks."""
    tasks = HousekeepingService.list_tasks()
    return jsonify([to_dict(t) for t in tasks])


@api_bp.route('/tasks/<int:tid>', methods=['GET'])
def get_task(tid: int):
    task = db.session.get(HousekeepingTask, tid)
    if not task:
        raise NotFound()
    return jsonify(to_dict(task))


@api_bp.route('/tasks/', methods=['POST'])
def create_task_api():
    data = require_json('room_id', 'due_date')
    task = HousekeepingService.schedule_task(data['room_id'], _parse_date(data['due_date']))
    resp = jsonify(to_dict(task))
    resp.status_code = 201
    return resp


@api_bp.route('/tasks/<int:tid>', methods=['PATCH'])
def complete_task_api(tid: int):
    data = require_json('completed')
    task = db.session.get(HousekeepingTask, tid)
    if not task:
        raise NotFound()
    if data.get('completed'):
        HousekeepingService.complete_task(tid)
    task = db.session.get(HousekeepingTask, tid)
    return jsonify(to_dict(task))

