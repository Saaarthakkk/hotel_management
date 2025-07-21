"""initial tables"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=80), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
    )
    op.create_table(
        'room',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('number', sa.String(length=10), nullable=False, unique=True),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
    )
    op.create_table(
        'booking',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('room_id', sa.Integer, sa.ForeignKey('room.id')),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date, nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='reserved'),
    )


def downgrade():
    op.drop_table('booking')
    op.drop_table('room')
    op.drop_table('user')
