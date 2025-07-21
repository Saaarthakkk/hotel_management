# PLAN: REST endpoints for Room resource using RoomService.
from __future__ import annotations

from datetime import datetime
from flask import jsonify, url_for
from werkzeug.exceptions import NotFound

from . import api_bp
from .schemas import to_dict, require_json
from ..services.room_service import RoomService
from ..models import db, Room


@api_bp.route('/rooms/', methods=['GET'])
def list_rooms_api():
    """Return all rooms."""
    rooms = RoomService.list_rooms()
    return jsonify([to_dict(r) for r in rooms])


@api_bp.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id: int):
    """Return single room or 404."""
    room = db.session.get(Room, room_id)
    if not room:
        raise NotFound()
    return jsonify(to_dict(room))


@api_bp.route('/rooms/', methods=['POST'])
def create_room_api():
    """Create a new room."""
    data = require_json('number', 'status')
    room = RoomService.create_room(data['number'], data['status'])
    resp = jsonify(to_dict(room))
    resp.status_code = 201
    resp.headers['Location'] = url_for('api_v1.get_room', room_id=room.id)
    return resp


@api_bp.route('/rooms/<int:room_id>', methods=['PATCH'])
def update_room_api(room_id: int):
    """Partially update a room."""
    room = db.session.get(Room, room_id)
    if not room:
        raise NotFound()
    data = require_json()
    RoomService.update_room(room_id, number=data.get('number'), status=data.get('status'))
    room = db.session.get(Room, room_id)
    return jsonify(to_dict(room))


@api_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room_api(room_id: int):
    """Delete a room."""
    RoomService.delete_room(room_id)
    return '', 204

