"""housekeeping recurring tasks and cleaning log link"""
from alembic import op
import sqlalchemy as sa

revision = '0006'
down_revision = '0005_booking_audit'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('housekeeping_task', sa.Column('booking_id', sa.Integer, sa.ForeignKey('booking.id')))
    op.add_column('housekeeping_task', sa.Column('recurrence_days', sa.Integer))
    op.add_column('cleaning_log', sa.Column('booking_id', sa.Integer, sa.ForeignKey('booking.id')))


def downgrade() -> None:
    op.drop_column('cleaning_log', 'booking_id')
    op.drop_column('housekeeping_task', 'recurrence_days')
    op.drop_column('housekeeping_task', 'booking_id')
