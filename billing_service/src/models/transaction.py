from typing import Union

from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field, BaseModel
from choicesenum import ChoicesEnum


class TransactionTypes(ChoicesEnum):
    TRANSFER = "TRANSFER", "Transfer to another bank account"
    TOP_UP = "TOP_UP", "Topping up of the bank account"
    TOP_UP_BY_ANOTHER_CURRENCY = "TOP_UP_BY_ANOTHER_CURRENCY", (
        "Topping up of the bank account by another currency"
    )
    SUBSCRIPTION_PAYMENT = "SUBSCRIPTION_PAYMENT", "Subscription payment"


class SubscriptionPaymentTransactionType(BaseModel):
    description: str | TransactionTypes = TransactionTypes.SUBSCRIPTION_PAYMENT.display
    number_of_subscription_month: int
    currency: str
    amount: float


class TopUpTransactionType(BaseModel):
    pass


class TopUpTransactionByAnotherCurrencyType(BaseModel):
    bank_account_id: UUID
    description: str | TransactionTypes = TransactionTypes.TOP_UP_BY_ANOTHER_CURRENCY.display
    base_currency: str
    topped_up_amount_in_base_currency: float
    quote_currency: str
    credited_amount_in_quote_currency: float


class TransferTransactionType(BaseModel):
    description: str | TransactionTypes = TransactionTypes.TRANSFER.display
    amount: float
    currency: str
    transferred_to_profile_id: UUID
    transferred_to_bank_account_id: UUID


class Transaction(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    profile_id: UUID
    transaction: Union[
        SubscriptionPaymentTransactionType,
        TopUpTransactionByAnotherCurrencyType,
        # TransferTransactionType,
        # TopUpTransactionType,
    ]
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Settings:
        name = "transactions"

    class Config:
        str_strip_whitespace = True
