from __future__ import annotations
from typing import TYPE_CHECKING, Annotated

from fastapi import HTTPException, status
from sqlalchemy import Result, select

from src.models.bank_account import BankAccount
from src.models.profile import Profile
from src.utils.messages import messages
from src.utils import profile_crud, currency_pair_crud


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.schemas.bank_account import (
        BankAccountCreate,
        BankAccountRead,
    )


async def create_bank_account(
    bank_account_in: BankAccountCreate,
    user_id: str,
    session: AsyncSession,
) -> BankAccountRead:
    profile = await profile_crud.get_profile_by_user_id(user_id, session)
    bank_account = BankAccount(
        currency=bank_account_in.model_dump()["currency"].value,
        profile_id=profile.id,
    )
    session.add(bank_account)
    await session.commit()
    await session.refresh(bank_account)
    return bank_account


async def get_bank_account_by_id(
    bank_account_id: str,
    session: AsyncSession,
) -> BankAccount:
    stmt = select(BankAccount).where(BankAccount.id == bank_account_id)
    result: Result = await session.execute(stmt)
    bank_account: BankAccount = result.scalars().one_or_none()
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.BANK_ACCOUNT_WITH_THAT_ID_WAS_NOT_FOUND,
        )
    return bank_account


async def get_bank_accounts_by_user_id_through_profile_id(
    user_id: str,
    session: AsyncSession,
) -> list[BankAccount]:
    profile = await profile_crud.get_profile_by_user_id(user_id, session)
    stmt = select(BankAccount).where(BankAccount.profile_id == profile.id)
    result: Result = await session.execute(stmt)
    bank_accounts: list[BankAccount] = result.scalars().all()
    if not bank_accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.USER_PROFILE_BANK_ACCOUNTS_WERE_NOT_FOUND,
        )
    return bank_accounts


async def get_bank_account_by_user_id_through_profile_id_and_currency(
    user_id: str,
    currency: str,
    session: AsyncSession,
):
    profile: Profile = await profile_crud.get_profile_by_user_id(user_id, session)
    stmt = select(BankAccount).where(
        BankAccount.profile_id == profile.id,
        BankAccount.currency == currency,
    )
    result: Result = await session.execute(stmt)
    bank_account: BankAccount = result.scalars().one_or_none()
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.USER_PROFILE_BANK_ACCOUNT_WITH_CURRENCY_ENTERED_WAS_NOT_FOUND,
        )
    return bank_account


async def get_bank_accounts(
    session: AsyncSession,
    currency: str = None,
):
    if currency:
        stmt = select(BankAccount).where(BankAccount.currency == currency)
    else:
        stmt = select(BankAccount)

    result: Result = await session.execute(stmt)
    bank_accounts = result.scalars().all()
    if not bank_accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.BANK_ACCOUNTS_WERE_NOT_FOUND,
        )
    return bank_accounts


async def get_bank_accounts_by_profile_id(
    profile_id: str,
    session: AsyncSession,
) -> list[BankAccount]:
    stmt = select(BankAccount).where(BankAccount.profile_id == profile_id)
    result: Result = await session.execute(stmt)
    bank_accounts: list[BankAccount] = result.scalars().all()
    if not bank_accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.USER_PROFILE_BANK_ACCOUNTS_WERE_NOT_FOUND,
        )
    return bank_accounts


async def get_bank_account_by_profile_id_with_specified_currency(
    profile_id: str,
    currency: str,
    session: AsyncSession,
) -> BankAccount:
    stmt = select(BankAccount).where(
        BankAccount.profile_id == profile_id,
        BankAccount.currency == currency,
    )
    result: Result = await session.execute(stmt)
    bank_account: BankAccount = result.scalars().one_or_none()
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.PROFILE_WITH_SPECIFIED_ID_DOES_NOT_HAVE_BANK_ACCOUNT_WITH_THAT_CURRENCY,
        )
    return bank_account


async def get_bank_account_by_profile_and_bank_account_id(
    profile_id: str,
    bank_account_id: str,
    session: AsyncSession,
) -> BankAccountRead:
    stmt = select(BankAccount).where(
        BankAccount.profile_id == profile_id,
        BankAccount.id == bank_account_id,
    )
    result: Result = await session.execute(stmt)
    bank_account: BankAccount = result.scalars().one_or_none()
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.PROFILE_WITH_SPECIFIED_ID_DOES_NOT_HAVE_BANK_ACCOUNT_WITH_THAT_ID,
        )
    return bank_account


async def delete_bank_account_by_id(
    user_id: str,
    bank_account_id: str,
    session: AsyncSession,
):
    profile: Profile = await profile_crud.get_profile_by_user_id(
        user_id,
        session,
    )
    bank_account = await get_bank_account_by_id(
        bank_account_id,
        session,
    )

    if not bank_account.profile_id == profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=messages.USER_DOES_NOT_HAVE_APPROPRIATE_PERMISSIONS,
        )

    await session.delete(bank_account)
    await session.commit()


async def delete_bank_account_by_admin(
    bank_account_id: str,
    session: AsyncSession,
):
    bank_account = await get_bank_account_by_id(
        bank_account_id,
        session,
    )
    await session.delete(bank_account)
    await session.commit()


async def delete_profile_bank_accounts(
    profile_id: str,
    session: AsyncSession,
):
    bank_accounts = await get_bank_accounts_by_profile_id(
        profile_id,
        session,
    )

    for bank_account in bank_accounts:
        await session.delete(bank_account)

    await session.commit()


async def update_bank_account_balance(
    bank_account_profile_id: str,
    bank_account_currency: str,
    amount_to_top_up: float,
    session: AsyncSession,
):
    bank_account: BankAccount = await get_bank_account_by_profile_id_with_specified_currency(
        bank_account_profile_id,
        bank_account_currency,
        session,
    )
    bank_account.balance += amount_to_top_up
    await session.commit()
    return bank_account
