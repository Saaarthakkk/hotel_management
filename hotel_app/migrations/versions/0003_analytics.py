"""add rate strategies and overbooking plan"""
from alembic import op
import sqlalchemy as sa

revision = '0003_analytics'
down_revision = '0002_housekeeping'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'rate_strategy',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('plan_id', sa.Integer, sa.ForeignKey('rate_plan.id')),
        sa.Column('type', sa.String(length=20)),
        sa.Column('active', sa.Boolean, nullable=False, server_default='1'),
    )
    op.create_table(
        'bar_rate',
        sa.Column('id', sa.Integer, sa.ForeignKey('rate_strategy.id'), primary_key=True),
        sa.Column('discount', sa.Float),
    )
    op.create_table(
        'package_rate',
        sa.Column('id', sa.Integer, sa.ForeignKey('rate_strategy.id'), primary_key=True),
        sa.Column('package', sa.String(length=50)),
        sa.Column('discount', sa.Float),
    )
    op.create_table(
        'corporate_rate',
        sa.Column('id', sa.Integer, sa.ForeignKey('rate_strategy.id'), primary_key=True),
        sa.Column('corp_code', sa.String(length=20)),
        sa.Column('discount', sa.Float),
    )
    op.create_table(
        'overbooking_plan',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, unique=True, nullable=False),
        sa.Column('limit', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('overbooking_plan')
    op.drop_table('corporate_rate')
    op.drop_table('package_rate')
    op.drop_table('bar_rate')
    op.drop_table('rate_strategy')
