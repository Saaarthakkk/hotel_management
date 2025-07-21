# PLAN: add rate strategy polymorphism and overbooking plan models
from __future__ import annotations

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt


db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User of the hotel management system."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='available')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='reserved', nullable=False)
    user = db.relationship('User', backref='bookings')
    room = db.relationship('Room', backref='bookings')


class GuestProfile(db.Model):
    """Stores guest preferences and history."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    preferences = db.Column(db.Text)
    stay_history = db.Column(db.Text)
    user = db.relationship('User', backref='profile', uselist=False)


class HousekeepingTask(db.Model):
    """Scheduled housekeeping tasks."""
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    priority = db.Column(db.Integer, default=1, nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    completed_at = db.Column(db.DateTime)
    room = db.relationship('Room', backref='hk_tasks')
    assignee = db.relationship('User', backref='hk_tasks', foreign_keys=[assigned_to])


class RatePlan(db.Model):
    """Rates for dynamic pricing."""
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(20), unique=True)
    base_rate = db.Column(db.Float, nullable=False)
    dynamic_rate = db.Column(db.Float)


class CleaningLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('housekeeping_task.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    duration = db.Column(db.Integer)
    task = db.relationship('HousekeepingTask', backref='logs')


class RateStrategy(db.Model):
    """Polymorphic rate strategy base. HL: inheritance/polymorphism."""

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('rate_plan.id'))
    type = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True)
    plan = db.relationship('RatePlan', backref='strategies')
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "base"}


class BARRate(RateStrategy):
    __tablename__ = 'bar_rate'
    id = db.Column(db.Integer, db.ForeignKey('rate_strategy.id'), primary_key=True)
    discount = db.Column(db.Float, default=0.0)
    __mapper_args__ = {"polymorphic_identity": "bar"}


class PackageRate(RateStrategy):
    __tablename__ = 'package_rate'
    id = db.Column(db.Integer, db.ForeignKey('rate_strategy.id'), primary_key=True)
    package = db.Column(db.String(50))
    discount = db.Column(db.Float, default=0.0)
    __mapper_args__ = {"polymorphic_identity": "package"}


class CorporateRate(RateStrategy):
    __tablename__ = 'corporate_rate'
    id = db.Column(db.Integer, db.ForeignKey('rate_strategy.id'), primary_key=True)
    corp_code = db.Column(db.String(20))
    discount = db.Column(db.Float, default=0.0)
    __mapper_args__ = {"polymorphic_identity": "corporate"}


class OverbookingPlan(db.Model):
    """Stores computed oversell limits."""

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
