from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.transaction import (
    TransactionCreate,
    TransactionRead,
)
from src.db.postgres import db_helper
from src.utils import transaction_crud, auth_utils
from src.schemas.transaction import TransactionHistoryEntry
from src.models.transaction import Transaction


router = APIRouter()


@router.get(
    "/history/",
    response_model=list[TransactionHistoryEntry],
)
async def get_profile_transaction_history_entries(
    # user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
):
    """
    Get transaction history entries

    Return value:
    - **transaction_history_entries** (list[TransactionHistoryEnty]): list of
    transaction history entry
    """
    user_id = UUID("1f6f3a5e-0968-4acd-840c-e10bd2b4508a")
    transaction_history_entries = await Transaction.find(
        Transaction.user_id == user_id,
    ).to_list()
    return transaction_history_entries


@router.post(
    "/create/phonenumber/{phone_number}/",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionRead,
)
async def create_transaction_by_receipent_phonenumber(
    transaction_in: TransactionCreate,
    phone_number: Annotated[str, Path(description="Receipent phonenumber")],
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create transaction by receipent phone_number
    """
    return await transaction_crud.create_transaction_by_receipent_phonenumber(
        transaction_in,
        phone_number,
        user_id,
        session,
    )
