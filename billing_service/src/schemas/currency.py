from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from choicesenum import ChoicesEnum
# from sqlalchemy_utils import CurrencyType


class CurrencyTitleDescription(ChoicesEnum):
    RUB = "RUB", "Russian Ruble"
    USD = "USD", "US Dollar"
    EUR = "EUR", "Euro"
    CNY = "CNY", "Chinese Yuan"
    PNT = "PNT", "Built-in Point"


class CurrencyBase(BaseModel):
    title: CurrencyTitleDescription


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyRead(CurrencyBase):
    id: UUID
    title: str
    description: str
    updated_at: datetime
    created_at: datetime
