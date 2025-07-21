from __future__ import annotations

from flask import Blueprint

from .auth import bp as auth_bp
from .rooms import bp as rooms_bp
from .bookings import bp as bookings_bp
from .housekeeping import bp as housekeeping_bp

__all__ = [
    'auth_bp',
    'rooms_bp',
    'bookings_bp',
    'housekeeping_bp',
]
