from __future__ import annotations

import logging

from flask import Blueprint, render_template, redirect, url_for

from ..services.pricing_service import PricingService
from ..utils import login_required, roles_required, setup_logger
from ..forms import RoomForm

from ..models import db, Room
from ..services.room_service import RoomService

bp = Blueprint('rooms', __name__, url_prefix='/rooms')
logger = setup_logger(__name__, 'rooms.log')


@bp.route('/')
@login_required
def list_rooms() -> str:
    """List rooms with current dynamic rates."""
    PricingService.update_dynamic_rates()
    rooms = db.session.query(Room).all()
    rates = {room.type: PricingService.get_rate(room.type) for room in rooms}
    return render_template('rooms.html', rooms=rooms, rates=rates)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'manager')
def new_room():
    """Create a new room."""
    form = RoomForm()
    if form.validate_on_submit():
        RoomService.create_room(form.number.data, form.type.data)
        return redirect(url_for('rooms.list_rooms'))
    return render_template('new_room.html', form=form)

