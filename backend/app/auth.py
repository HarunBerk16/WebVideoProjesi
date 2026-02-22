from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException, status

from .config import settings
from .schemas import Role


TOKEN_TTL_MINUTES = 120


def create_participant_token(room_id: str, participant_id: str, role: Role) -> str:
    now = datetime.now(tz=UTC)
    payload = {
        "room_id": room_id,
        "participant_id": participant_id,
        "role": role.value,
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_TTL_MINUTES),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
    return payload
