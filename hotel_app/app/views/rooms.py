from __future__ import annotations

import logging
import os

from flask import Blueprint, render_template

from ..services.pricing_service import PricingService
from ..utils import login_required

from ..services.room_service import RoomService

bp = Blueprint('rooms', __name__, url_prefix='/rooms')
logger = logging.getLogger(__name__)
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'rooms.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
handler = logging.FileHandler(log_path)
logger.addHandler(handler)


@bp.route('/')
@login_required
def list_rooms():
    PricingService.update_dynamic_rates()
    rooms = RoomService.list_rooms()
    rates = {room.type: PricingService.get_rate(room.type) for room in rooms}
    return render_template('rooms.html', rooms=rooms, rates=rates)
