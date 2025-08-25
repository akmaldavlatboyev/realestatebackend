"""add phone to otp_codes

Revision ID: 3283b8964173
Revises: af21f22ba8fb
Create Date: 2025-08-25 11:16:03.361060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3283b8964173'
down_revision: Union[str, None] = 'af21f22ba8fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    with op.batch_alter_table("otp_codes") as batch_op:
        batch_op.add_column(sa.Column("phone", sa.String(), nullable=True))
        batch_op.create_index(batch_op.f("ix_otp_codes_phone"), ["phone"], unique=False)
        batch_op.drop_column("user_id")


def downgrade() -> None:
    with op.batch_alter_table("otp_codes") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.drop_index(batch_op.f("ix_otp_codes_phone"))
        batch_op.drop_column("phone")
