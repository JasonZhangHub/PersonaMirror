from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )
    passcode_salt = Column(String(64), nullable=False)
    passcode_hash = Column(String(128), nullable=False)
    alias = Column(String(128), nullable=True)
    age = Column(Integer, nullable=True)
    education = Column(String(128), nullable=True)
    gender = Column(String(64), nullable=True)
    consent_signed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    bfi2_responses = relationship(
        "BFI2Response",
        back_populates="user",
        cascade="all, delete-orphan",
    )
