from __future__ import annotations

from typing import Optional

from ..models import User, db


class AuthService:
    """Service for CRUD operations on users."""

    @staticmethod
    def create_user(username: str, password: str, role: str) -> User:
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_password(user: User, password: str) -> None:
        user.set_password(password)
        db.session.commit()

    @staticmethod
    def delete_user(user_id: int) -> None:
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
