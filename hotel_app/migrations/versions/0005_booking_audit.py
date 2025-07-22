"""add booking audit trail"""
from alembic import op
import sqlalchemy as sa

revision = '0005_booking_audit'
down_revision = '0004_user_email_active'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('booking', sa.Column('cancelled_at', sa.DateTime))
    op.create_table(
        'booking_audit',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('booking_id', sa.Integer, sa.ForeignKey('booking.id')),
        sa.Column('action', sa.String(length=50)),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('details', sa.String(length=200)),
    )


def downgrade() -> None:
    op.drop_table('booking_audit')
    op.drop_column('booking', 'cancelled_at')
