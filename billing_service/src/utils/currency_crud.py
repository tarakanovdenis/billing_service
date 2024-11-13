from __future__ import annotations
from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from sqlalchemy import select, Result

from src.models.currency import Currency
from src.utils.messages import messages


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.schemas.currency import (
        CurrencyCreate,
        CurrencyRead,
    )


async def create_currency(
    currency_in: CurrencyCreate,
    session: AsyncSession,
) -> CurrencyRead:
    currency = Currency(
        **currency_in.model_dump(),
    )
    session.add(currency)
    await session.commit()
    await session.refresh(currency)

    return currency


async def get_currency_by_id(
    currency_id: str,
    session: AsyncSession,
) -> Currency | None:
    stmt = select(Currency).where(Currency.id == currency_id)
    result: Result = await session.execute(stmt)
    currency: Currency = result.scalars().one_or_none()
    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.CURRENCY_WITH_THAT_ID_WAS_NOT_FOUND,
        )

    return currency


async def get_currencies(
    session: AsyncSession,
) -> list[Currency] | None:
    stmt = select(Currency)
    result: Result = await session.execute(stmt)
    currencies: list[Currency] = result.scalars().all()
    if not currencies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.CURRENCY_ENTRIES_WERE_NOT_FOUND,
        )

    return currencies


async def get_currency_by_title(
    currency_title: str,
    session: AsyncSession,
) -> Currency | None:
    stmt = select(Currency).where(Currency.title == currency_title)
    result: Result = await session.execute(stmt)
    currency: Currency = result.scalars().one_or_none()
    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.SPECIFIED_CURRENCY_WAS_NOT_FOUND
        )

    return currency


async def delete_currency(
    currency_id: str,
    session: AsyncSession,
):
    currency: Currency = await get_currency_by_id(currency_id, session,)
    await session.delete(currency)
    await session.commit()
