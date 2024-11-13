from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    String,
    Float,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

# from sqlalchemy_utils import CurrencyType

from src.models.base import Base, TimestampMixin


if TYPE_CHECKING:
    from src.models.profile import Profile
    from src.models.transaction import Transaction


class BankAccount(TimestampMixin, Base):
    __tablename__ = "bank_accounts"

    __table_args__ = (
        CheckConstraint(
            "balance >= 0",
            name="ck_bank_accounts_balance_more_than_zero",
        ),
        UniqueConstraint(
            "profile_id",
            "currency",
            name="uq_bank_accounts_profile_id_currency"
        ),
    )

    balance: Mapped[float] = mapped_column(
        Float(precision=2),
        default=0,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )
    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE")
    )

    profile: Mapped[Profile] = relationship(
        "Profile",
        back_populates="bank_accounts",
    )

    repr_columns = (
        "id",
        "profile_id",
        "balance",
        "currency",
        "created_at",
    )
