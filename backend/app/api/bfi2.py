from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.bfi2 import BFI2Response
from app.models.user import User
from app.schemas.bfi2 import (
    BFI2ResponseCreate,
    BFI2ResponseOut,
    BFI2ResponseUpdate,
)
from scripts.analysis.bfi2_scorer import BFI2Scorer

router = APIRouter(tags=["bfi2"])


def _normalize_responses(responses: dict[int, int]) -> dict[int, int]:
    return {int(key): int(value) for key, value in responses.items()}


def _validate_responses(responses: dict[int, int]) -> None:
    invalid = [
        key
        for key, value in responses.items()
        if value < 1 or value > 5
    ]
    if invalid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Responses must be between 1 and 5.",
        )


def _load_questions() -> dict[str, Any]:
    backend_root = Path(__file__).resolve().parents[2]
    questions_path = backend_root / "data" / "bfi2" / "questions.json"
    if not questions_path.exists():
        raise FileNotFoundError("Questions not found.")
    return json.loads(questions_path.read_text())


@router.get("/bfi2/questions")
def get_questions() -> dict[str, Any]:
    try:
        return _load_questions()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/bfi2/responses",
    response_model=BFI2ResponseOut,
    status_code=status.HTTP_201_CREATED,
)
def create_response(
    payload: BFI2ResponseCreate,
    db: Session = Depends(get_db),
) -> BFI2ResponseOut:
    user = db.execute(
        select(User).where(User.id == payload.user_id)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    responses = _normalize_responses(payload.responses)
    _validate_responses(responses)
    scorer = BFI2Scorer()
    scored = scorer.score(responses, persona=user.participant_id).to_dict()

    response = BFI2Response(
        user_id=user.id,
        survey_type=payload.survey_type,
        responses=responses,
        scored=scored,
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return response


@router.get(
    "/bfi2/responses/{response_id}",
    response_model=BFI2ResponseOut,
)
def get_response(
    response_id: int,
    db: Session = Depends(get_db),
) -> BFI2ResponseOut:
    response = db.execute(
        select(BFI2Response).where(BFI2Response.id == response_id)
    ).scalar_one_or_none()
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found.",
        )
    return response


@router.get(
    "/bfi2/users/{user_id}/responses",
    response_model=list[BFI2ResponseOut],
)
def list_user_responses(
    user_id: int,
    db: Session = Depends(get_db),
) -> list[BFI2ResponseOut]:
    responses = db.execute(
        select(BFI2Response)
        .where(BFI2Response.user_id == user_id)
        .order_by(BFI2Response.created_at.desc())
    ).scalars().all()
    return responses


@router.put(
    "/bfi2/responses/{response_id}",
    response_model=BFI2ResponseOut,
)
def update_response(
    response_id: int,
    payload: BFI2ResponseUpdate,
    db: Session = Depends(get_db),
) -> BFI2ResponseOut:
    response = db.execute(
        select(BFI2Response).where(BFI2Response.id == response_id)
    ).scalar_one_or_none()
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)
    if "responses" in update_data:
        normalized = _normalize_responses(update_data["responses"])
        _validate_responses(normalized)
        scorer = BFI2Scorer()
        response.responses = normalized
        response.scored = scorer.score(
            normalized,
            persona=str(response.user_id),
        ).to_dict()

    if "survey_type" in update_data:
        response.survey_type = update_data["survey_type"]

    db.add(response)
    db.commit()
    db.refresh(response)
    return response


@router.delete(
    "/bfi2/responses/{response_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_response(response_id: int, db: Session = Depends(get_db)) -> Response:
    response = db.execute(
        select(BFI2Response).where(BFI2Response.id == response_id)
    ).scalar_one_or_none()
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found.",
        )

    db.delete(response)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
