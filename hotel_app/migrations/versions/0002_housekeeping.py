"""extend housekeeping tables"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('housekeeping_task', sa.Column('assigned_to', sa.Integer, sa.ForeignKey('user.id')))
    op.add_column('housekeeping_task', sa.Column('priority', sa.Integer, nullable=False, server_default='1'))
    op.add_column('housekeeping_task', sa.Column('completed_at', sa.DateTime))
    op.create_table(
        'cleaning_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('housekeeping_task.id')),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('duration', sa.Integer),
    )


def downgrade():
    op.drop_table('cleaning_log')
    op.drop_column('housekeeping_task', 'completed_at')
    op.drop_column('housekeeping_task', 'priority')
    op.drop_column('housekeeping_task', 'assigned_to')
