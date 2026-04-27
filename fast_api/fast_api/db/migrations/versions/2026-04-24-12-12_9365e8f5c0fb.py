"""add users and saved weather tables

Revision ID: 9365e8f5c0fb
Revises: 819cbf6e030b
Create Date: 2026-04-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "9365e8f5c0fb"
down_revision = "819cbf6e030b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("username", sa.String(100), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "saved_weather",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("country", sa.String(10), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("feels_like", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("wind_speed", sa.Float(), nullable=False),
        sa.Column("icon", sa.String(20), nullable=False),
        sa.Column(
            "saved_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_saved_weather_user_id", "saved_weather", ["user_id"])


def downgrade() -> None:
    op.drop_table("saved_weather")
    op.drop_table("users")