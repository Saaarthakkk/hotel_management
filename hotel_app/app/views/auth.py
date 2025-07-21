from __future__ import annotations

import logging
import os

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from ..services.auth_service import AuthService
from ..utils import login_required

bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'auth.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
handler = logging.FileHandler(log_path)
logger.addHandler(handler)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate(form.username.data, form.password.data)
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('rooms.list_rooms'))
        logger.info('Failed login for %s', form.username.data)
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
