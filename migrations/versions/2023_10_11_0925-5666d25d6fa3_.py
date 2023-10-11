"""empty message

Revision ID: 5666d25d6fa3
Revises: 2ac5a5afd402
Create Date: 2023-10-11 09:25:25.806035

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5666d25d6fa3"
down_revision: Union[str, None] = "2ac5a5afd402"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "file",
        sa.Column("link", sa.String(), nullable=False),
        sa.Column("public_id", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=True),
        sa.Column("file_type", sa.String(), nullable=False),
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("file")
    # ### end Alembic commands ###
