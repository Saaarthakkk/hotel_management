# PLAN: Blueprint providing JSON REST API with API key auth and error handlers.
from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound

api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_bp.before_request
def require_api_key() -> None:
    """Validate static API key."""
    key = current_app.config.get('API_KEY', 'secret')
    if request.headers.get('X-API-Key') != key:
        raise Unauthorized('invalid API key')


@api_bp.errorhandler(BadRequest)
def handle_bad_request(err: BadRequest):
    return jsonify(error=str(err.description or 'bad request')), 400


@api_bp.errorhandler(Unauthorized)
def handle_unauth(err: Unauthorized):
    return jsonify(error=str(err.description or 'unauthorized')), 401


@api_bp.errorhandler(NotFound)
def handle_not_found(err: NotFound):
    return jsonify(error='not found'), 404


from . import rooms, bookings, housekeeping  # noqa: E402

