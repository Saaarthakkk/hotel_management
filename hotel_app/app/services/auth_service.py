from __future__ import annotations

from typing import Optional

from ..models import User, db


class AuthService:
    """Service for user authentication management."""

    @staticmethod
    def create_user(username: str, password: str, role: str) -> User:
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
