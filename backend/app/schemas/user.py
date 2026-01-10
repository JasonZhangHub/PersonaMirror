from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    participant_id: str = Field(min_length=3, max_length=64)
    passcode: str = Field(min_length=4, max_length=128)


class UserLogin(BaseModel):
    participant_id: str
    passcode: str


class UserUpdate(BaseModel):
    alias: str | None = Field(default=None, max_length=128)
    age: int | None = Field(default=None, ge=18, le=120)
    education: str | None = Field(default=None, max_length=128)
    gender: str | None = Field(default=None, max_length=64)
    consented: bool | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    participant_id: str
    alias: str | None
    age: int | None
    education: str | None
    gender: str | None
    consent_signed_at: datetime | None
    created_at: datetime
    updated_at: datetime
