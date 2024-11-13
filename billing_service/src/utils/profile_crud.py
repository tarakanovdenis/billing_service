from __future__ import annotations
from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from sqlalchemy import Result, select

from src.models.profile import Profile
from src.utils.messages import messages


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.schemas.profile import (
        ProfileCreate,
        ProfileUpdate,
    )


async def get_profile_by_user_id(
    user_id: str,
    session: AsyncSession,
) -> Profile:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result: Result = await session.execute(stmt)
    profile: Profile = result.scalars().one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.USER_PROFILE_WAS_NOT_FOUND
        )

    return profile


async def get_profile_by_profile_id(
    profile_id: str,
    session: AsyncSession,
) -> Profile:
    stmt = select(Profile).where(Profile.id == profile_id)
    result: Result = await session.execute(stmt)
    profile: Profile = result.scalars().one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.USER_PROFILE_WAS_NOT_FOUND
        )

    return profile


async def get_profile_by_email(
    email: str,
    session: AsyncSession,
) -> Profile | None:
    stmt = select(Profile).where(Profile.email == email)
    result: Result = await session.execute(stmt)
    profile: Profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.USER_PROFILE_WITH_THAT_EMAIL_WAS_NOT_FOUND,
        )

    return profile


async def create_profile(
    profile_in: ProfileCreate,
    user_id: str,
    session: AsyncSession,
) -> Profile:

    profile = Profile(
        **profile_in.model_dump(),
        user_id=user_id,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)

    return profile


async def get_profile(
    user_id: str,
    session: AsyncSession,
) -> Profile:
    return await get_profile_by_user_id(
        user_id,
        session,
    )


async def get_profiles(
    session: AsyncSession,
) -> list[Profile]:
    stmt = select(Profile)
    result: Result = await session.execute(stmt)
    profiles: list[Profile] = result.scalars().all()
    if not profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=messages.USER_PROFILES_WERE_NOT_FOUND,
        )
    return profiles


async def update_profile(
    profile_update: ProfileUpdate,
    user_id: str,
    session: AsyncSession,
) -> Profile:
    profile: Profile = await get_profile_by_user_id(user_id, session)
    for name, value in profile_update.model_dump(exclude_unset=True).items():
        setattr(profile, name, value)
    await session.commit()
    return profile


async def delete_profile_by_user_id(
    user_id: str,
    session: AsyncSession,
) -> None:
    profile: Profile = await get_profile_by_user_id(user_id, session)
    await session.delete(profile)
    await session.commit()


async def delete_profile_by_profile_id(
    profile_id: str,
    session: AsyncSession,
) -> None:
    profile: Profile = await get_profile_by_profile_id(profile_id, session)
    await session.delete(profile)
    await session.commit()
