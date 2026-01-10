from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class BFI2Response(Base):
    __tablename__ = "bfi2_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    survey_type = Column(String(32), nullable=False, default="pre")
    responses = Column(JSON, nullable=False)
    scored = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="bfi2_responses")
