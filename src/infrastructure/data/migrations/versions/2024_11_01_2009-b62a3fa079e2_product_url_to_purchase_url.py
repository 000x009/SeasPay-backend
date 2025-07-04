"""product_url to purchase_url

Revision ID: b62a3fa079e2
Revises: bd7a3f0c25b5
Create Date: 2024-11-01 20:09:40.865748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b62a3fa079e2'
down_revision: Union[str, None] = 'bd7a3f0c25b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('digital_product_details', sa.Column('purchase_url', sa.String(), nullable=False))
    op.drop_column('digital_product_details', 'product_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('digital_product_details', sa.Column('product_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('digital_product_details', 'purchase_url')
    # ### end Alembic commands ###
