from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Role(str, Enum):
    THERAPIST = "therapist"
    CLIENT = "client"


class CreateRoomRequest(BaseModel):
    therapist_id: str = Field(min_length=3)
    client_id: str = Field(min_length=3)


class ParticipantTokenResponse(BaseModel):
    room_id: str
    role: Role
    token: str


class CreateRoomResponse(BaseModel):
    room_id: str
    therapist: ParticipantTokenResponse
    client: ParticipantTokenResponse


class IceServer(BaseModel):
    urls: list[str]
    username: str | None = None
    credential: str | None = None


class IceConfigResponse(BaseModel):
    ice_servers: list[IceServer]


class SignalingMessage(BaseModel):
    type: Literal["offer", "answer", "ice-candidate", "ping", "ready"]
    payload: dict = Field(default_factory=dict)
