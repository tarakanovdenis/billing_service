from __future__ import annotations
from typing import TYPE_CHECKING

from src.models.transaction import (
    Transaction,
    TopUpTransactionByAnotherCurrencyType,
    SubscriptionPaymentTransactionType,
)
from src.utils.messages import messages


if TYPE_CHECKING:
    from uuid import UUID


async def create_top_up_bank_account_by_another_currency_transaction_history_entry(
    user_id: UUID,
    profile_id: UUID,
    profile_bank_account_id: UUID,
    base_currency: str,
    quote_currency: str,
    topped_up_amount_in_base_currency: float,
    credited_amount_in_quote_currency: float,
):
    transaction = Transaction(
        user_id=user_id,
        profile_id=profile_id,
        transaction=TopUpTransactionByAnotherCurrencyType(
            bank_account_id=profile_bank_account_id,
            base_currency=base_currency,
            topped_up_amount_in_base_currency=topped_up_amount_in_base_currency,
            quote_currency=quote_currency,
            credited_amount_in_quote_currency=credited_amount_in_quote_currency,
        ),
    )
    _: Transaction = await transaction.create()
    return {
        "details": messages.TRANSACTION_HISTORY_ENTRY_WAS_CREATED,
    }


async def create_subcription_payment_transaction_history_entry(
    user_id: UUID,
    profile_id: UUID,
    number_of_subscription_month: int,
    currency: str,
    amount: float,
):
    transaction = Transaction(
        user_id=user_id,
        profile_id=profile_id,
        transaction=SubscriptionPaymentTransactionType(
            number_of_subscription_month=number_of_subscription_month,
            currency=currency,
            amount=amount,
        )
    )
    _: Transaction = await transaction.create()
    return {
        "details": messages.TRANSACTION_HISTORY_ENTRY_WAS_CREATED,
    }
