from typing import Annotated

from fastapi import APIRouter, status, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import db_helper
from src.schemas.bank_account import (
    BankAccountRead,
    BankAccountCreate,
)
from src.utils import bank_account_crud
from src.schemas.currency import CurrencyTitleDescription


router = APIRouter()


@router.post(
    "/create/{profile_id}/",
    status_code=status.HTTP_201_CREATED,
    response_model=BankAccountRead,
)
async def create_bank_account_by_profile_id(
    bank_account_in: BankAccountCreate,
    profile_id: Annotated[str, Path(description="Profile ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create bank account using profile ID [admin permissions]

    Parameters:
    - **profile_id** (str): existing profile ID (UUID4)

    Return value:
    - **bank_account** (BankAccountRead): created profile's bank account entity

    """
    return await bank_account_crud.create_bank_account(
        bank_account_in,
        profile_id,
        session,
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[BankAccountRead],
)
async def get_bank_accounts(session: AsyncSession = Depends(db_helper.get_session)):
    """
    Get all bank accounts [admin permissions]

    Return value:
    - **bank_accounts** (list[BankAccountRead]): list of bank accounts
    """
    return await bank_account_crud.get_bank_accounts(session)


@router.get(
    "/currency/{currency}/",
    status_code=status.HTTP_200_OK,
    response_model=list[BankAccountRead],
)
async def get_bank_accounts_with_specified_currency(
    currency: Annotated[CurrencyTitleDescription, Path(description="Currency")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get all bank accounts with the specified currency [admin permissions]

    Parameters:
    - **currency** (CurrencyTitleDescription): "USD", "RUB", "CNY", "EUR" or "PNT"

    Return value:
    - **bank_accounts** (list[BankAccountRead]): list of bank accounts with
        the specified currency
    """
    return await bank_account_crud.get_bank_accounts(
        session,
        currency=currency.value,
    )


@router.get(
    "/profile/{profile_id}/",
    status_code=status.HTTP_200_OK,
    response_model=list[BankAccountRead],
)
async def get_user_profile_bank_accounts(
    profile_id: Annotated[str, Path(description="Profile ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get user profile bank accounts using profile ID [admin permissions]

    Parameters:
    - **profile_id** (str): existing profile ID (UUID4)

    Return value:
    - **bank_accounts** (list[BankAccountRead]): list of profile's bank accounts
    """
    return await bank_account_crud.get_bank_accounts_by_profile_id(
        profile_id,
        session,
    )


@router.get(
    "/profile/{profile_id}/currency/{currency}/",
    status_code=status.HTTP_200_OK,
    response_model=BankAccountRead,
)
async def get_user_profile_bank_account_with_specified_currency(
    profile_id: Annotated[str, Path(description="Profile ID (UUID4)")],
    currency: Annotated[CurrencyTitleDescription, Path(description="Currency")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get user profile bank accounts with the specified currency [admin permissions]

    Parameters:
    - **profile_id** (str): existing profile ID (UUID4)
    - **currency** (CurrencyTitleDescription): "USD", "RUB", "CNY", "EUR" or "PNT"
    """
    return await bank_account_crud.get_bank_account_by_profile_id_with_specified_currency(
        profile_id,
        currency.value,
        session,
    )


@router.get(
    "/profile/{profile_id}/bank-account/{bank_account_id}/",
    status_code=status.HTTP_200_OK,
    response_model=BankAccountRead,
)
async def get_user_profile_bank_account_by_profile_and_bank_account_ids(
    profile_id: Annotated[str, Path(description="Profile ID (UUID4)")],
    bank_account_id: Annotated[str, Path(description="Bank Account ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get user profile bank account [admin permissions]

    Parameters:
    - **profile_id** (str): existing profile ID (UUID4)
    - **bank_account_id** (str): existing profile bank account ID (UUID4)

    Return value:
    - **bank_account** (BankAccountRead): bank account entity
    """
    return await bank_account_crud.get_bank_account_by_profile_id_with_specified_currency(
        profile_id,
        bank_account_id,
        session,
    )


@router.delete(
    "/delete/{bank_account_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bank_account(
    bank_account_id: Annotated[str, Path(description="Bank Account ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete bank account [admin permissions]

    Parameters:
    - **bank_account_id** (str): exitsting bank account ID (UUID4)
    """
    return await bank_account_crud.delete_bank_account_by_admin(
        bank_account_id,
        session,
    )


@router.delete(
    "/delete/profile/{profile_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile_bank_accounts(
    profile_id: Annotated[str, Path(description="Profile ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete all profile's bank accounts

    Parameters:
    - **profile_id** (str): existing profile ID (UUID4)
    """
    return await bank_account_crud.delete_profile_bank_accounts(
        profile_id,
        session
    )
