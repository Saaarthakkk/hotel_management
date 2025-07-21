from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for, session, Response
from flask_login import LoginManager, login_user, logout_user, current_user, login_required as flask_login_required

from ..forms import LoginForm, RegistrationForm
from ..services.auth_service import AuthService
from ..models import db, User
from ..utils import role_required, setup_logger

bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = setup_logger(__name__, 'auth.log')
login_manager = LoginManager()


@bp.record_once
def init(state) -> None:
    login_manager.init_app(state.app)
    login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))


@bp.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data, duration=None)
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('rooms.list_rooms'))
        logger.info('Failed login for %s', form.username.data)
    return render_template('login.html', form=form)


@bp.route('/logout')
@flask_login_required
def logout() -> Response:
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
@flask_login_required
@role_required('admin')
def register() -> Response:
    form = RegistrationForm()
    if form.validate_on_submit():
        AuthService.create_user(form.username.data, form.password.data, form.role.data)
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
