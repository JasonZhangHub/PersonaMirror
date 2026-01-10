from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BFI2ResponseCreate(BaseModel):
    user_id: int
    survey_type: str = Field(default="pre", max_length=32)
    responses: dict[int, int]


class BFI2ResponseUpdate(BaseModel):
    survey_type: str | None = Field(default=None, max_length=32)
    responses: dict[int, int] | None = None


class BFI2ResponseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    survey_type: str
    responses: dict[int, int]
    scored: dict[str, Any]
    created_at: datetime
    updated_at: datetime
