from sqlalchemy import String, DateTime, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy_utils import CurrencyType

from src.models.base import Base, TimestampMixin
from src.schemas.currency import CurrencyTitleDescription


class Currency(TimestampMixin, Base):
    __tablename__ = "currencies"

    title: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(128),
        nullable=True,
    )

    base_currencies: Mapped["CurrencyPair"] = relationship(
        "CurrencyPair",
        back_populates="base_currency",
        passive_deletes=True,
        foreign_keys="CurrencyPair.base_currency_id",
    )
    quote_currencies: Mapped["CurrencyPair"] = relationship(
        "CurrencyPair",
        back_populates="quote_currency",
        passive_deletes=True,
        foreign_keys="CurrencyPair.quote_currency_id",
    )

    repr_columns = (
        "id",
        "title",
        "created_at",
    )

    def __init__(self, title: CurrencyTitleDescription):
        self.title = title.value
        self.description = title.display


class CurrencyPair(TimestampMixin, Base):
    __tablename__ = "currency_pairs"

    __table_args__ = (
        UniqueConstraint(
            "base_currency_id",
            "quote_currency_id",
            name="uq_currency_pairs_base_currency_id_quote_currency_id",
        ),
    )

    base_currency_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "currencies.id",
            ondelete="CASCADE",
            name="fk_currency_pairs_base_currency_id_currencies_id",
        ),
        nullable=False,
    )
    quote_currency_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "currencies.id",
            ondelete="CASCADE",
            name="fk_currency_pairs_quote_currency_id_currencies_id",
        ),
        nullable=False,
    )
    exchange_rate: Mapped[float] = mapped_column(
        Float(precision=4),
        nullable=False,
    )

    base_currency: Mapped[Currency] = relationship(
        "Currency",
        back_populates="base_currencies",
        foreign_keys=[base_currency_id],
    )

    quote_currency: Mapped[Currency] = relationship(
        "Currency",
        back_populates="quote_currencies",
        foreign_keys=[quote_currency_id],
    )

    repr_columns = (
        "id",
        "base_currency_id",
        "quote_curency_id",
        "exchange_rate",
        "updated_at",
        "created_at",
    )
