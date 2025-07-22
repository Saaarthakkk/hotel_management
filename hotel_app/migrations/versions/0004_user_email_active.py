"""add email and active to user"""
from alembic import op
import sqlalchemy as sa

revision = '0004_user_email_active'
down_revision = '0003_analytics'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('email', sa.String(length=120), nullable=False, server_default=''))
    op.add_column('user', sa.Column('active', sa.Boolean, nullable=False, server_default='0'))
    op.alter_column('user', 'email', server_default=None)


def downgrade() -> None:
    op.drop_column('user', 'active')
    op.drop_column('user', 'email')
