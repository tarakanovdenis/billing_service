from typing import Annotated

from fastapi import APIRouter, status, Path, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import db_helper

from src.schemas.currency_pair import (
    CurrencyPairCreate,
    CurrencyPairRead,
    CurrencyPairUpdate,
)
from src.utils import currency_pair_crud


router = APIRouter()


@router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=CurrencyPairRead,
)
async def create_currency_pair(
    currency_pair_in: CurrencyPairCreate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create currency pair [admin permissions]

    Parameters:
    - **base_currency_id** (UUID): existing currency UUID
    - **quote_currency_id** (UUID): existing currency UUID
    - **exchange_rate** (float): float value at which one currency
    an be converted into another

    Return value:
    - **currency_pair** (CurrencyPairRead): currency pair entity
    """
    return await currency_pair_crud.create_currency_pair(
        currency_pair_in,
        session,
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[CurrencyPairRead],
)
async def get_currency_pairs(
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get currency pairs [admin permissions]

    Return value:
    - **currency_pairs** (list[CurrencyPairRead]): list of currency pairs
    """
    return await currency_pair_crud.get_currency_pairs(session)


@router.get(
    "/{currency_pair_id}/",
    status_code=status.HTTP_200_OK,
    response_model=CurrencyPairRead,
)
async def get_currency_pair(
    currency_pair_id: Annotated[str, Path(description="Currency pair ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get currency pair by ID [admin permissions]

    Parameters:
    - **currency_pair_id** (str): existing currency pair ID (UUID)
    """
    return await currency_pair_crud.get_currency_pair_by_id(
        currency_pair_id,
        session,
    )


@router.patch(
    "/update/{currency_pair_id}",
    response_model=CurrencyPairRead,
)
async def update_currency_pair_partially(
    currency_pair_id: Annotated[str, Path(description="Currency pair ID (UUID4)")],
    currency_pair_update: CurrencyPairUpdate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Update currency pair by ID [admin permissions]

    Parameters:
    - **currency_pair_id** (str): existing currency pair ID (UUID4)
    - **currency_pair_update** (CurrencyPairUpdate): currency pair entity for
    partilly updating **exchange_rate**
    """
    return await currency_pair_crud.update_currency_pair_by_id(
        currency_pair_id,
        currency_pair_update,
        session,
    )


# It is presented as an example, later it is needed to use third-party API
# to get exchange rate values between USD and another currencies
exchange_rates = {
    "USD/RUB": 97.303,
    "USD/EUR": 0.9200,
    "USD/CNY": 7.1195,
}


@router.post(
    "/set-exchange-rates/",
)
async def set_exchange_rates(
    exchange_rate_usd_to_point: float = 50,
    exchange_rates_to_usd: dict[str, float] = exchange_rates,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Set exchange rate between all existing currencies and Point currency

    Parameters:
    - **exchange_rate_usd_to_point** (float): exchange rate value between USD
    and built-in "Point" currency
    - **exchange rates to usd** (dict[str, float]): exchange rate values between
    USD and other currencies to set exchange rate between built-in "Point"
    currency and other currencies
    """
    return await currency_pair_crud.set_exchange_rate_currencies_to_point_currency(
        exchange_rate_usd_to_point,
        exchange_rates_to_usd,
        session=session,
    )
