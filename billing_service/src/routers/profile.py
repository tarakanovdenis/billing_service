from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import db_helper
from src.schemas.profile import (
    ProfileCreate,
    ProfileRead,
    ProfileUpdate,
)
from src.utils import auth_utils, profile_crud


router = APIRouter()


@router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileRead,
)
async def create_user_profile(
    profile_in: ProfileCreate,
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create profile

    Return value:
        **profile** (ProfileRead): profile with the following fields:
        id, user_id, first_name, last_name, phone_number, email, date_of_birth
    """
    return await profile_crud.create_profile(profile_in, user_id, session)


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    response_model=ProfileRead,
)
async def get_user_profile(
    session: AsyncSession = Depends(db_helper.get_session),
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
):
    """
    Get profile information

    Return value:
        **profile** (ProfileRead): profile with the following fields:
        id, user_id, first_name, last_name, phone_number, email, date_of_birth
    """
    return await profile_crud.get_profile(user_id, session)


@router.patch(
    "/update/",
    response_model=ProfileRead,
)
async def update_profile_partially(
    profile_update: ProfileUpdate,
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Update profile partially

    Parameter:
    - **user_id** (str): existing user ID (UUID4)
    - **profile_update** (ProfileUpdate): profile entity for partilly updating
    **first_name**, **last_name**, **phone_number**, **email**,
    **date_of_birth**
    """
    return await profile_crud.update_profile(
        profile_update,
        user_id,
        session,
    )


@router.delete(
    "/delete/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile(
    user_id: str = Depends(auth_utils.get_current_auth_user_id_from_or_401),
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete profile using user ID from auth JWT

    Parameters:
    - **user_id** (str): existing user ID (UUID4)
    """
    await profile_crud.delete_profile_by_user_id(user_id, session)
