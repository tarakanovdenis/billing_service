from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel, EmailStr, ConfigDict


class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    date_of_birth: date | None = None


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: UUID
    user_id: UUID
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    date_of_birth: date | None = None
