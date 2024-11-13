from uuid import UUID
from datetime import datetime
from typing import Union
from pydantic import BaseModel

from src.schemas.currency import CurrencyTitleDescription
from src.models.transaction import TransactionTypes
from src.models.transaction import (
    SubscriptionPaymentTransactionType,
    TopUpTransactionByAnotherCurrencyType,
    TopUpTransactionType,
)

class TransactionBase(BaseModel):
    pass


class SubscriptionPaymentTransaction(BaseModel):
    description: TransactionTypes = TransactionTypes.SUBSCRIPTION_PAYMENT.display
    number_of_subscription_month: int
    currency: str
    amount: float


class TopUpTransactionByAnotherCurrency(BaseModel):
    bank_account_id: UUID
    description: TransactionTypes = TransactionTypes.TOP_UP_BY_ANOTHER_CURRENCY.display
    base_currency: str
    topped_up_amount_in_base_currency: float
    quote_currency: str
    credited_amount_in_quote_currency: float


class TransactionHistoryEntry(BaseModel):
    id: UUID
    user_id: UUID
    profile_id: UUID
    transaction: Union[
        # SubscriptionPaymentTransaction,
        # TopUpTransactionByAnotherCurrency,
        SubscriptionPaymentTransactionType,
        TopUpTransactionByAnotherCurrencyType,
        # TopUpTransactionType,
    ]
    timestamp: datetime


class TransactionCreate(BaseModel):
    amount: float
    currency: CurrencyTitleDescription


class TransactionRead(BaseModel):
    id: UUID
    amount: float
    currency: str
    profile_id: UUID
    bank_account_id: UUID
    timestamp: datetime


class TopUpTransactionByAnotherCurrency(BaseModel):
    currency: CurrencyTitleDescription
    point_amount: float


class SubscriptionPaymentTransaction(BaseModel):
    number_of_subscription_month: int
    amount: float
