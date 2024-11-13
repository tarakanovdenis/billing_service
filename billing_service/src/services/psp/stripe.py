from decimal import Decimal

import stripe
from fastapi import Request
from typing_extensions import override

from src.core.config import settings
from src.services.psp.abc import PaymentServiceProvider


stripe.api_key = settings.stripe_payment_service.stripe_secret_key
stripe.api_version = settings.stripe_payment_service.stripe_api_version


class StripeProvider(PaymentServiceProvider):
    @override
    def get_top_up_bank_account_by_another_currency_checkout_session(
        self,
        currency: str,
        amount_in_currency: float,
        amount_in_point_currency: float,
        user_id: str,
        profile_id: str,
        email: str,
    ):
        return stripe.checkout.Session.create(
            customer_creation="always",
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": "Balance account top-up",
                        },
                        "unit_amount": int(amount_in_currency * 100),
                    },
                    "quantity": 1,
                },
            ],
            phone_number_collection={"enabled": True},
            customer_email=email,
            mode="payment",

            success_url=(
                f"http://127.0.0.1:8001/billing/bank-account/top-up/success?currency={currency}&amount={amount_in_currency}&point_amount={amount_in_point_currency}"
            ),
            cancel_url="http://127.0.0.1:8001/billing/bank-account/top-up/cancel/",

            saved_payment_method_options={
                "payment_method_save": "enabled",
            },
            metadata={
                "user_id": user_id,
                "profile_id": profile_id,
                "amount_in_point_currency": amount_in_point_currency,
            }
        )

    @override
    def get_subscription_payment_checkout_session(
        self,
        number_of_subscription_month: int,
        amount: float,
        email: str,
        user_id: str,
        profile_id: str,
        currency: str = "USD",
    ):
        return stripe.checkout.Session.create(
            customer_creation="always",
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": (
                                f"Subscription payment - {number_of_subscription_month} month(s)"),
                        },
                        "unit_amount": int(amount * 100),
                    },
                    "quantity": 1,
                },
            ],
            phone_number_collection={"enabled": True},
            customer_email=email,
            mode="payment",

            success_url=(
                f"http://127.0.0.1:8001/billing/payment/subscription/success?month_number={number_of_subscription_month}&amount={amount}"
            ),
            cancel_url="http://127.0.0.1:8001/billing/payment/subscription/cancel",
            saved_payment_method_options={
                "payment_method_save": "enabled",
            },
            metadata={
                "user_id": user_id,
                "profile_id": profile_id,
                "number_of_subscription_month": number_of_subscription_month,
                "currency": currency,
                "amount": amount,
            }
        )


def get_stripe_provider():
    return StripeProvider()
