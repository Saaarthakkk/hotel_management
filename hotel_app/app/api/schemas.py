# PLAN: Serialization helpers converting models to dicts and validating JSON.
from __future__ import annotations

from flask import request
from werkzeug.exceptions import BadRequest


def to_dict(obj, include_relations: bool = False) -> dict:
    """Serialize SQLAlchemy model to dictionary."""
    data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    if include_relations:
        for rel in obj.__mapper__.relationships:
            val = getattr(obj, rel.key)
            if val is None:
                data[rel.key] = None
            elif isinstance(val, list):
                data[rel.key] = [to_dict(i, False) for i in val]
            else:
                data[rel.key] = to_dict(val, False)
    return data


def require_json(*fields: str) -> dict:
    """Return JSON data ensuring required fields are present."""
    if not request.is_json:
        raise BadRequest('JSON required')
    data = request.get_json() or {}
    if not isinstance(data, dict):
        raise BadRequest('JSON body must be object')
    for field in fields:
        if field not in data:
            raise BadRequest(f'missing field {field}')
    return data

