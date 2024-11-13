from typing import Annotated

from fastapi import APIRouter, status, Path, Depends
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
    "/create/{user_id}/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileRead,
)
async def create_user_profile(
    profile_in: ProfileCreate,
    user_id: Annotated[str, Path(description="User ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Create profile by user id [admin permissions]

    Return value:
    - **profile** (ProfileRead): profile with the following fields:
        id, user_id, first_name, last_name, phone_number, email, date_of_birth
    """
    return await profile_crud.create_profile(profile_in, user_id, session)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProfileRead],
)
async def get_profiles(
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get profiles [admin permissions]

    Return value:
    - **profiles** (list[ProfileRead]): list of profiles
    """
    return await profile_crud.get_profiles(session)


@router.get(
    "/user/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ProfileRead,
)
async def get_user_profile_by_user_id(
    user_id: Annotated[str, Path(description="User ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get user profile using user ID [admin permissions]

    Parameters:
    - **user_id** (str): existing user ID (UUID4)

    Return value:
    - **profile** (ProfileRead): user's profile
    """
    return await profile_crud.get_profile_by_user_id(user_id, session)


@router.get(
    "/{profile_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ProfileRead,
)
async def get_user_profile_by_profile_id(
    profile_id: Annotated[str, Path(description="Profile ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Get user profile using profile ID [admin permissions]

    Parameters:
    - **profile_id** (str): existing profile ID (UUID4)

    Return value:
    - **profile** (ProfileRead): profile entity
    """
    return await profile_crud.get_profile_by_profile_id(profile_id, session)


@router.delete(
    "/delete/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile_by_user_id(
    user_id: Annotated[str, Path(description="User ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete user profile using user ID [admin permissions]

    Parameters:
    - **user_id** (str): existing profile's user id
    """
    await profile_crud.delete_profile_by_user_id(user_id, session)


@router.delete(
    "/delete/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile_by_profile_id(
    profile_id: Annotated[str, Path(description="Profile ID (UUID4)")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    """
    Delete user profile using profile ID [admin permissions]

    Parameters:
    - **profile_id** (str): existing profile ID (UUID4)
    """
    await profile_crud.delete_profile_by_profile_id(profile_id, session)
