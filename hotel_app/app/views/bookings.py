from __future__ import annotations

import logging
import os

from flask import Blueprint

bp = Blueprint('bookings', __name__, url_prefix='/bookings')
logger = logging.getLogger(__name__)
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'bookings.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
handler = logging.FileHandler(log_path)
logger.addHandler(handler)
