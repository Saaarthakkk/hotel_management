from __future__ import annotations

import logging
import os

from flask import Blueprint

bp = Blueprint('housekeeping', __name__, url_prefix='/housekeeping')
logger = logging.getLogger(__name__)
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'housekeeping.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
handler = logging.FileHandler(log_path)
logger.addHandler(handler)
