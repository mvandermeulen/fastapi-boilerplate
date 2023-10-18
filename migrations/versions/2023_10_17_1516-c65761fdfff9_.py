"""empty message

Revision ID: c65761fdfff9
Revises:
Create Date: 2023-10-17 15:16:44.910595

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c65761fdfff9"
down_revision: Union[str, None] = None
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
    op.create_table(
        "role",
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("label", sa.String(length=255), nullable=True),
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
    op.create_table(
        "casbinrule",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ptype", sa.String(length=255), nullable=True),
        sa.Column("v0", sa.String(length=255), nullable=True),
        sa.Column("v1", sa.String(length=255), nullable=True),
        sa.Column("v2", sa.String(length=255), nullable=True),
        sa.Column("v3", sa.String(length=255), nullable=True),
        sa.Column("v4", sa.String(length=255), nullable=True),
        sa.Column("v5", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["v0"],
            ["role.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("firstname", sa.String(length=64), nullable=True),
        sa.Column("lastname", sa.String(length=64), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("email_verified", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column("role_id", sa.String(length=32), nullable=True),
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["role.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_firstname"), "user", ["firstname"], unique=False)
    op.create_index(op.f("ix_user_lastname"), "user", ["lastname"], unique=False)
    op.create_index(op.f("ix_user_phone"), "user", ["phone"], unique=False)
    op.create_table(
        "notification",
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("viewed", sa.Boolean(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_notification_content"), "notification", ["content"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_notification_content"), table_name="notification")
    op.drop_table("notification")
    op.drop_index(op.f("ix_user_phone"), table_name="user")
    op.drop_index(op.f("ix_user_lastname"), table_name="user")
    op.drop_index(op.f("ix_user_firstname"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("casbinrule")
    op.drop_table("role")
    op.drop_table("file")
    # ### end Alembic commands ###
