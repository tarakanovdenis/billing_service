from typing import Annotated
import json

import stripe
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    responses,
    status,
    Depends,
    Path,
    Query,
    Form,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.bank_account import BankAccountCreate, BankAccountRead
from src.utils import (
    auth_utils,
    bank_account_crud,
    profile_crud,
    transaction_crud,
    currency_pair_crud,
)
from src.db.postgres import db_helper
from src.schemas.currency import CurrencyTitleDescription
from src.schemas.transaction import TopUpTransactionByAnotherCurrency
from src.services.psp.stripe import StripeProvider, get_stripe_provider
from src.core.config import BASE_DIR
from src.utils.messages import messages


router = APIRouter()

templates = Jinja2Templates(directory=BASE_DIR / "static" / "templates")


@router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=BankAccountRead,
)
async def create_bank_account(
    bank_account_in: BankAccountCreate,
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create bank account using user ID from auth JWT

    Parameters:
    - **user_id** (str): existing user ID (UUID4)
    - **currency** (CurrencyTitleDescription): "USD", "RUB", "CNY", "EUR" or "PNT"

    Return value:
    - **bank_account** (BankAccountRead): created profile's bank account entity

    """
    return await bank_account_crud.create_bank_account(
        bank_account_in,
        user_id,
        session,
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[BankAccountRead],
)
async def get_user_bank_accounts(
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get user profile bank accounts using user ID from auth JWT through
    profile ID

    Parameters:
    - **user_id** (str): existing user ID (UUID4)

    Return value:
    - **bank_accounts** (list[BankAccountRead]): list of profile's bank accounts
    """
    return await bank_account_crud.get_bank_accounts_by_user_id_through_profile_id(
        user_id,
        session,
    )


@router.get(
    "/currency/{currency}/",
    status_code=status.HTTP_200_OK,
    response_model=BankAccountRead,
)
async def get_user_bank_account_with_currency(
    currency: Annotated[CurrencyTitleDescription, Path(description="Currency")],
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get user profile bank account with the specified currency using user ID
    from auth JWT through profile ID

    Parameters:
    - **user_id** (str): existing user ID (UUID4)
    - **currency** (CurrencyTitleDescription): "USD", "RUB", "CNY", "EUR" or "PNT"

    Return value:
    - **bank_account** (BankAccountRead): profile's bank account with
    the specified currency
    """
    return await bank_account_crud.get_bank_account_by_user_id_through_profile_id_and_currency(
        user_id, currency.value, session
    )


@router.delete(
    "/delete/{bank_account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_bank_account(
    bank_account_id: Annotated[str, Path(description="Bank account ID (UUID4)")],
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete profile bank account using bank account ID and user ID from auth JWT

    Parameters:
    - **bank_account_id** (str): exitsting bank account ID (UUID4)
    """
    return await bank_account_crud.delete_bank_account_by_id(
        user_id, bank_account_id, session
    )


@router.get(
    "/top-up/",
)
async def top_up_bank_account(
    request: Request,
):
    """
    HTML template page for user's topping up his "Point" currency bank account
    """
    return templates.TemplateResponse(
        request=request,
        name="top_up_transaction.html"
    )


@router.post(
    "/top-up/create/",
)
async def create_top_up_bank_account(
    top_up_transaction: Annotated[TopUpTransactionByAnotherCurrency, Form()],
    payment_service_provider: Annotated[StripeProvider, Depends(get_stripe_provider)],
    # user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Top up bank account with built-in currency Point using any available currency

    Parameters:
    - **top_up_transaction** (TopUpTransactionByAnotherCurrency): desired
    **amount** of built-in "Point" currency and **currency** - currency, from
    converting which, bank account in built-in "Point" currency will be topped up
    """
    user_id = "1f6f3a5e-0968-4acd-840c-e10bd2b4508a"
    profile = await profile_crud.get_profile_by_user_id(
        user_id,
        session,
    )

    top_up_transaction_dict = top_up_transaction.model_dump()

    amount_in_base_currency = await currency_pair_crud.get_amount_in_base_currency_using_quote_currency(
        top_up_transaction_dict["currency"].value,
        top_up_transaction_dict["point_amount"],
        session,
    )

    checkout_session_url = payment_service_provider.get_top_up_bank_account_by_another_currency_checkout_session(
        top_up_transaction_dict["currency"].value,
        amount_in_base_currency,
        top_up_transaction_dict["point_amount"],
        user_id,
        profile.id,
        profile.email,
    )

    return responses.RedirectResponse(
        checkout_session_url.url,
        status_code=status.HTTP_303_SEE_OTHER,
    )
    # return checkout_session_url.url


@router.post(
    "/top-up/webhook/",
)
async def transaction_processing_webhook(
    request: Request,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Webhook endpoint for tracking confirmation from the Stripe Payment System
    and updating bank account
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

            # To send email about transaction result
            # profile_email = checkout_session.customer_details.email
            user_id: str = checkout_session.metadata.user_id
            profile_id: str = checkout_session.metadata.profile_id
            base_currency: str = checkout_session.currency
            amount_in_base_currency: float = checkout_session.amount_total / 100
            amount_in_quote_currency: float = float(
                checkout_session.metadata.amount_in_point_currency
            )

            updated_bank_account = await bank_account_crud.update_bank_account_balance(
                profile_id,
                CurrencyTitleDescription.PNT.value,
                amount_in_quote_currency,
                session,
            )

            result = await transaction_crud.create_top_up_bank_account_by_another_currency_transaction_history_entry(
                user_id,
                profile_id,
                updated_bank_account.id,
                base_currency.upper(),
                CurrencyTitleDescription.PNT.value,
                amount_in_base_currency,
                amount_in_quote_currency,
            )

    return responses.Response(
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/top-up/success",
    response_class=responses.HTMLResponse,
)
async def top_up_transaction_success(
    request: Request,
    currency: Annotated[str, Query(description="Currency to be topped up")],
    amount: Annotated[float, Query(description="Currency amount")],
    point_amount: Annotated[float, Query(description="Amount in Point currency")],
):
    """
    HTML template page to show that the top-up transaction has been successfully completed
    """
    return templates.TemplateResponse(
        request=request,
        name="top_up_transaction_success.html",
        context={
            "currency": currency,
            "amount": int(amount),
            "point_amount": int(point_amount),
        },
    )


@router.get(
    "/top-up/cancel/",
    response_class=responses.HTMLResponse,
)
async def top_up_transaction_canceled(
    request: Request,
):
    """
    HTML template page to show that the top-up transaction has been cancelled
    """
    return templates.TemplateResponse(
        request=request,
        name="top_up_transaction_cancelled.html",
    )
