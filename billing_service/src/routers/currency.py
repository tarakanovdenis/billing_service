from typing import Annotated

from fastapi import APIRouter, status, Path, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import db_helper
from src.schemas.currency import CurrencyCreate, CurrencyRead
from src.utils import currency_crud


router = APIRouter()


@router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=CurrencyRead
)
async def create_currency(
    currency_in: CurrencyCreate,
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create currency entry [admin permission]

    Parameter:
    - **currency_in**: currency title - "USD", "RUB", "EUR", "CNY" or "PNT"
    """
    return await currency_crud.create_currency(currency_in, session)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[CurrencyRead],
)
async def get_currency_entries(
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get currency entries [admin permission]

    Return value:
    - **currencies** (list[CurrencyRead]): list of the existing currencies
    """
    return await currency_crud.get_currencies(session)


@router.get(
    "/{currency_id}",
    status_code=status.HTTP_200_OK,
    response_model=CurrencyRead,
)
async def get_currency_entry(
    currency_id: Annotated[str, Path(description="Currency ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get currency entry details using ID [admin permission]

    Parameters:
    - **currency_id** (str): existing currency ID (UUID4)

    Return value:
    - **currency** (CurrencyRead): currency entry
    """
    return await currency_crud.get_currency_by_id(
        currency_id,
        session,
    )


@router.delete(
    "/delete/{currency_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_currency(
    currency_id: Annotated[str, Path(description="Currency ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete currency entry [admin permission]

    Parameters:
    - **currency_id** (str): existing currency ID (UUID4)
    """
    return await currency_crud.delete_currency(currency_id, session)
