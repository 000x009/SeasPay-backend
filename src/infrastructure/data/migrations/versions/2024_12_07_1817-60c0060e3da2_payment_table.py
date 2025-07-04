"""payment table

Revision ID: 60c0060e3da2
Revises: cf854fdbf70b
Create Date: 2024-12-07 18:17:38.371332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '60c0060e3da2'
down_revision: Union[str, None] = 'cf854fdbf70b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('ACTIVE', 'PAID', 'FAILED', name='payment_status').create(op.get_bind())
    op.create_table('payment',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('invoice_url', sa.String(), nullable=False),
    sa.Column('amount', sa.DECIMAL(), nullable=False),
    sa.Column('status', postgresql.ENUM('ACTIVE', 'PAID', 'FAILED', name='payment_status', create_type=False), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('order', sa.Column('payment_id', sa.UUID(), nullable=True))
    op.alter_column('order', 'payment_receipt',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_foreign_key(None, 'order', 'payment', ['payment_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.alter_column('order', 'payment_receipt',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('order', 'payment_id')
    op.drop_table('payment')
    sa.Enum('ACTIVE', 'PAID', 'FAILED', name='payment_status').drop(op.get_bind())
    # ### end Alembic commands ###
