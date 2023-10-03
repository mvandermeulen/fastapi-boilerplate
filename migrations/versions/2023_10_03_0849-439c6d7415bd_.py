"""empty message

Revision ID: 439c6d7415bd
Revises:
Create Date: 2023-10-03 08:49:02.345424

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "439c6d7415bd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("firstname", sa.String(length=64), nullable=False),
        sa.Column("lastname", sa.String(length=64), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("email_verified", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
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
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_firstname"), "users", ["firstname"], unique=False)
    op.create_index(op.f("ix_users_lastname"), "users", ["lastname"], unique=False)
    op.create_index(op.f("ix_users_phone"), "users", ["phone"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_phone"), table_name="users")
    op.drop_index(op.f("ix_users_lastname"), table_name="users")
    op.drop_index(op.f("ix_users_firstname"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
