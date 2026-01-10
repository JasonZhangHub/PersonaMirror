from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_passcode, verify_passcode
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut

router = APIRouter(tags=["auth"])


@router.post(
    "/auth/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    existing = db.execute(
        select(User).where(User.participant_id == payload.participant_id)
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Participant ID already exists.",
        )

    salt, hashed = hash_passcode(payload.passcode)
    user = User(
        participant_id=payload.participant_id,
        passcode_salt=salt,
        passcode_hash=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=UserOut)
def login_user(payload: UserLogin, db: Session = Depends(get_db)) -> UserOut:
    user = db.execute(
        select(User).where(User.participant_id == payload.participant_id)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if not verify_passcode(
        payload.passcode,
        user.passcode_salt,
        user.passcode_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid passcode.",
        )

    return user
