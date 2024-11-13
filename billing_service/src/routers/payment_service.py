from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
import json

from fastapi import APIRouter, Depends, Form, Query, status, HTTPException, responses, Request
from fastapi.templating import Jinja2Templates
import stripe
import aiohttp

from src.core.config import BASE_DIR, settings
from src.utils import auth_utils, profile_crud, transaction_crud
from src.db.postgres import db_helper
from src.services.psp.stripe import StripeProvider, get_stripe_provider
from src.schemas.transaction import SubscriptionPaymentTransaction
from src.utils.messages import messages


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


templates = Jinja2Templates(directory=BASE_DIR / "static" / "templates")


@router.get(
    "/subscription/",
)
async def subscription_payment_page(
    request: Request,
):
    """
    HTML templage page for making a subscription payment transaction
    """
    return templates.TemplateResponse(
        request=request,
        name="subscription_payment.html",
    )


@router.post(
    "/subscription/create/",
)
async def create_subscription_payment(
    subscription_payment_transaction: Annotated[SubscriptionPaymentTransaction, Form()],
    payment_service_provider: Annotated[StripeProvider, Depends(get_stripe_provider)],
    # user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Creating subscription payment

    Parameters:
    - **number_of_subscription_month** (int): number of subscription months
    - **amount** (float): price for subscription
    """
    user_id = "1f6f3a5e-0968-4acd-840c-e10bd2b4508a"
    profile = await profile_crud.get_profile_by_user_id(
        user_id,
        session,
    )
    subscription_payment_transaction_dict = subscription_payment_transaction.model_dump()
    checkout_session_url = payment_service_provider.get_subscription_payment_checkout_session(
        subscription_payment_transaction_dict["number_of_subscription_month"],
        subscription_payment_transaction_dict["amount"],
        profile.email,
        user_id,
        profile.id,
    )
    return responses.RedirectResponse(
        checkout_session_url.url,
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post(
    "/subscription/webhook/",
)
async def subscription_payment_processing_webhook(
    request: Request,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Webhook endpoint for tracking confirmation from the Stripe Payment System
    and change user subscriber status
    """
    payload = await request.body()
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload),
            stripe.api_key,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.INVALID_REQUEST_PAYLOAD_DURING_CONSTRUCT_STRIPE_EVENT,
        )
    except stripe.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.INVALID_SIGNATURE_DURING_CONSTRUCT_STRIPE_EVENT,
        )

    if event.type == "checkout.session.completed":
        checkout_session = event.data.object

        if checkout_session.payment_status == "paid":
            user_id = checkout_session.metadata.user_id
            profile_id = checkout_session.metadata.profile_id
            number_of_subscription_month = checkout_session.metadata.number_of_subscription_month
            currency = checkout_session.metadata.currency
            amount = checkout_session.metadata.amount

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        f"{settings.auth_service_domain}/auth/subscription/user/{user_id}/create"
                    ) as response:
                        response.raise_for_status()
                        data = await response.json()

                        return data

                except aiohttp.ClientResponseError as e:
                    raise HTTPException(
                        status_code=e.status,
                        detail=str(e),
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=str(e),
                    )
                finally:
                    result = await transaction_crud.create_subcription_payment_transaction_history_entry(
                        user_id,
                        profile_id,
                        number_of_subscription_month,
                        currency,
                        amount
                    )


@router.get(
    "/subscription/success",
)
async def success(
    request: Request,
    month_number: Annotated[int, Query(description="Subscription month number")],
    amount: Annotated[float, Query(description="Subscription price for the specified time period")],
):
    """
    HTML template page to show that the subscription payment transaction has been successfully completed
    """
    return templates.TemplateResponse(
        request=request,
        name="subscription_payment_success.html",
        context={
            "month_number": month_number,
            "amount": int(amount),
        }
    )


@router.get(
    "/subscription/cancel/",
)
async def cancel(
    request: Request,
):
    """
    HTML template page to show that the subscription payment transaction has been cancelled
    """
    return templates.TemplateResponse(
        request=request,
        name="subscription_payment_cancelled.html",
    )
