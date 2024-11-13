from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import Base, TimestampMixin


if TYPE_CHECKING:
    from src.models.bank_account import BankAccount


class Profile(TimestampMixin, Base):
    __tablename__ = "profiles"

    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False
    )
    date_of_birth: Mapped[Date] = mapped_column(Date(), nullable=True)

    bank_accounts: Mapped[list[BankAccount]] = relationship(
        "BankAccount",
        back_populates="profile",
        passive_deletes=True,
    )

    repr_columns = (
        "id",
        "user_id",
        "first_name",
        "last_name",
        "email",
        "phone_number"
    )
