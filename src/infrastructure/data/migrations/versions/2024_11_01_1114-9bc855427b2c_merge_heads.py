"""merge heads

Revision ID: 9bc855427b2c
Revises: a94c4eb704be, 4f8d1b9a7e69
Create Date: 2024-11-01 11:14:34.696680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bc855427b2c'
down_revision: Union[str, None] = ('a94c4eb704be', '4f8d1b9a7e69')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
