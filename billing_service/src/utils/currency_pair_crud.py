from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import select, Result
from sqlalchemy.dialects.postgresql import insert as pg_insert
from fastapi import HTTPException, status

from src.models.currency import Currency, CurrencyPair
from src.schemas.currency import CurrencyTitleDescription
from src.utils import currency_crud
from src.utils.messages import messages


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from billing_service.src.schemas.currency_pair import (
        CurrencyPairCreate,
        CurrencyPairRead,
    )


async def create_currency_pair(
    currency_pair_in: CurrencyPairCreate,
    session: AsyncSession,
) -> CurrencyPairRead:
    currency_pair = CurrencyPair(
        **currency_pair_in.model_dump()
    )
    session.add(currency_pair)
    await session.commit()
    await session.refresh(currency_pair)

    return currency_pair


async def get_currency_pairs(
    session: AsyncSession,
) -> list[CurrencyPairRead] | None:
    stmt = select(CurrencyPair)
    result: Result = await session.execute(stmt)
    currency_prices: list[CurrencyPair] = result.scalars().all()
    if not currency_prices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.CURRENCY_PAIRS_WERE_NOT_FOUND,
        )
    return currency_prices


async def get_currency_pair_by_id(
    currency_pair_id: str,
    session: AsyncSession,
) -> CurrencyPair | None:
    stmt = select(CurrencyPair).where(CurrencyPair.id == currency_pair_id)
    result: Result = await session.execute(stmt)
    currency_pair: CurrencyPair = result.scalars().one_or_none()
    if not currency_pair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.CURRENCY_PAIR_WITH_THAT_ID_NOT_FOUND,
        )

    return currency_pair


async def get_currency_pair_by_base_currency_id(
    base_currency_id: str,
    session: AsyncSession,
) -> CurrencyPair | None:
    stmt = select(CurrencyPair).where(
        CurrencyPair.base_currency_id == base_currency_id
    )
    result: Result = await session.execute(stmt)
    currency_pair: CurrencyPair = result.scalars().one_or_none()
    if not currency_pair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.CURRENCY_PAIR_WITH_THAT_BASE_CURRENCY_ID_WAS_NOT_FOUND,
        )

    return currency_pair


async def set_exchange_rate_currencies_to_point_currency(
    exchange_rate_usd_to_point: float,
    exchange_rates_to_usd: dict,
    session: AsyncSession,
):
    # Retreive Point currency to find it's id in the `data` dictionary forming
    point_currency: Currency = await currency_crud.get_currency_by_title(
        CurrencyTitleDescription.PNT.value, session
    )

    # Extend dictionary with USD and another currencies exchange rates with
    # USD/PNT exchange rate
    exchange_rates_to_usd["USD/PNT"] = exchange_rate_usd_to_point

    for exchange_rate_to_usd in exchange_rates_to_usd.items():

        # Set variables base_currency to USD and quote_currency to quote currency
        base_currency, quote_currency = exchange_rate_to_usd[0].split("/")

        # If quote currency is Point currency, then it is necessary to add
        # this currency pair (USD/PNT) to table without calculating exchange rate
        if quote_currency == "PNT":
            # Get currency to find it's id in `data` dictionary
            # in this case it is needed find id of USD currency
            base_currency: Currency = await currency_crud.get_currency_by_title(
                base_currency,
                session,
            )

            data = {
                "base_currency_id": base_currency.id,
                "quote_currency_id": point_currency.id,
                "exchange_rate": exchange_rate_usd_to_point,
            }
        else:
            # In this case it is needed to find ids of quote currencies in the
            # dictionary with USD and another currencies exchange rates
            base_currency: Currency = await currency_crud.get_currency_by_title(
                quote_currency,
                session,
            )
            data = {
                "base_currency_id": base_currency.id,
                "quote_currency_id": point_currency.id,
                "exchange_rate": exchange_rate_usd_to_point / exchange_rate_to_usd[1]
            }

        stmt = pg_insert(CurrencyPair).values(data)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_currency_pairs_base_currency_id_quote_currency_id",
            set_={
                "exchange_rate": stmt.excluded.exchange_rate
            }
        )

        await session.execute(stmt)

    await session.commit()
    return {
        "details": "Exchange rates have been established successfully."
    }


async def get_amount_in_quote_currency_using_base_currency(
    base_currency_title: str,
    amount_in_base_currency: float,
    session: AsyncSession,
):
    base_currency: Currency = await currency_crud.get_currency_by_title(
        base_currency_title,
        session,
    )
    currency_pair: CurrencyPair = await get_currency_pair_by_base_currency_id(
        base_currency.id,
        session,
    )
    amount_in_quote_currency = (
        currency_pair.exchange_rate * amount_in_base_currency
    )
    return amount_in_quote_currency


async def get_amount_in_base_currency_using_quote_currency(
    base_currency_title: str,
    amount_in_quote_currency: float,
    session: AsyncSession,
):
    base_currency: Currency = await currency_crud.get_currency_by_title(
        base_currency_title,
        session,
    )
    currency_pair: CurrencyPair = await get_currency_pair_by_base_currency_id(
        base_currency.id,
        session,
    )
    amount_in_base_currency = (
        amount_in_quote_currency / currency_pair.exchange_rate
    )
    return amount_in_base_currency
