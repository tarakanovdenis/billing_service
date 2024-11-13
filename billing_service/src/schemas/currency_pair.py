from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class CurrencyPairBase(BaseModel):
    exchange_rate: float


class CurrencyPairCreate(CurrencyPairBase):
    base_currency_id: UUID
    quote_currency_id: UUID


class CurrencyPairUpdate(CurrencyPairBase):
    pass


class CurrencyPairRead(CurrencyPairBase):
    id: UUID
    base_currency_id: UUID
    quote_currency_id: UUID
    updated_at: datetime
    created_at: datetime
