"""Utility helpers for role-based access."""

from __future__ import annotations

from functools import wraps
import logging
import os
from flask import session, redirect, url_for


def setup_logger(name: str, filename: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger writing to the logs folder."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        handler = logging.FileHandler(os.path.join(log_dir, filename))
        handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s'))
        handler.setLevel(level)
        logger.setLevel(level)
        logger.addHandler(handler)
    return logger


def role_required(role: str):
    """Decorator enforcing that the logged in user has a specific role."""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get('role') != role:
                return redirect(url_for('auth.login'))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def roles_required(*roles: str):
    """Decorator that allows several roles."""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get('role') not in roles:
                return redirect(url_for('auth.login'))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def login_required(view):
    """Simple login required decorator using session."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped

