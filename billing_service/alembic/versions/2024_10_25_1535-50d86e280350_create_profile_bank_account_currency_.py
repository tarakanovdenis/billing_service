"""create profile, bank_account, currency, currency_pair tables

Revision ID: 50d86e280350
Revises:
Create Date: 2024-10-25 15:35:57.570262

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "50d86e280350"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currencies",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=3), nullable=False),
        sa.Column("description", sa.String(length=128), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_currencies")),
        sa.UniqueConstraint("id", name=op.f("uq_currencies_id")),
        sa.UniqueConstraint("title", name=op.f("uq_currencies_title")),
    )
    op.create_table(
        "profiles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=False),
        sa.Column("last_name", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=32), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_profiles")),
        sa.UniqueConstraint("email", name=op.f("uq_profiles_email")),
        sa.UniqueConstraint("id", name=op.f("uq_profiles_id")),
        sa.UniqueConstraint(
            "phone_number", name=op.f("uq_profiles_phone_number")
        ),
        sa.UniqueConstraint("user_id", name=op.f("uq_profiles_user_id")),
    )
    op.create_table(
        "bank_accounts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("balance", sa.Float(precision=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("profile_id", sa.UUID(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "balance >= 0",
            name=op.f(
                "ck_bank_accounts_ck_bank_accounts_balance_more_than_zero"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.id"],
            name=op.f("fk_bank_accounts_profile_id_profiles"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_bank_accounts")),
        sa.UniqueConstraint("id", name=op.f("uq_bank_accounts_id")),
        sa.UniqueConstraint(
            "profile_id",
            "currency",
            name="uq_bank_accounts_profile_id_currency",
        ),
    )
    op.create_table(
        "currency_pairs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("base_currency_id", sa.UUID(), nullable=False),
        sa.Column("quote_currency_id", sa.UUID(), nullable=False),
        sa.Column("exchange_rate", sa.Float(precision=4), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["base_currency_id"],
            ["currencies.id"],
            name="fk_currency_pairs_base_currency_id_currencies_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["quote_currency_id"],
            ["currencies.id"],
            name="fk_currency_pairs_quote_currency_id_currencies_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_currency_pairs")),
        sa.UniqueConstraint(
            "base_currency_id",
            "quote_currency_id",
            name="uq_currency_pairs_base_currency_id_quote_currency_id",
        ),
        sa.UniqueConstraint("id", name=op.f("uq_currency_pairs_id")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("currency_pairs")
    op.drop_table("bank_accounts")
    op.drop_table("profiles")
    op.drop_table("currencies")
    # ### end Alembic commands ###
