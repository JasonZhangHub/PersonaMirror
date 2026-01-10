from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_passcode
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(tags=["users"])


@router.post(
    "/users",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
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


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)) -> list[UserOut]:
    users = db.execute(
        select(User).order_by(User.created_at.desc())
    ).scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> UserOut:
    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)
    consented = update_data.pop("consented", None)

    for key, value in update_data.items():
        setattr(user, key, value)

    if consented:
        user.consent_signed_at = datetime.now(timezone.utc)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
