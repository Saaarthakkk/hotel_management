import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import RatePlan, RateStrategy, BARRate, PackageRate


def test_polymorphic_queries():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        plan = RatePlan(room_type='std', base_rate=100, dynamic_rate=100)
        db.session.add(plan)
        db.session.commit()
        b = BARRate(plan_id=plan.id, discount=0.1)
        p = PackageRate(plan_id=plan.id, package='spa', discount=0.2)
        db.session.add_all([b, p])
        db.session.commit()
        types = {s.type for s in RateStrategy.query.all()}
        assert {'bar', 'package'} <= types
