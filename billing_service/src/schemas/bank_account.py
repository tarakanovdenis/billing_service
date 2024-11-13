from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from src.schemas.currency import CurrencyTitleDescription


class BankAccountBase(BaseModel):
    currency: CurrencyTitleDescription


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountRead(BankAccountBase):
    id: UUID
    profile_id: UUID
    balance: float
    updated_at: datetime
    created_at: datetime
