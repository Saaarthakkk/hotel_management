"""Utility helpers for role-based access."""

from __future__ import annotations

from functools import wraps
from flask import session, redirect, url_for


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


def login_required(view):
    """Simple login required decorator using session."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped

