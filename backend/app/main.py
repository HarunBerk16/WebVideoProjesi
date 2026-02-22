from __future__ import annotations

import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .auth import create_participant_token, verify_token
from .config import settings
from .room_manager import Participant, RoomManager
from .schemas import (
    CreateRoomRequest,
    CreateRoomResponse,
    IceConfigResponse,
    IceServer,
    ParticipantTokenResponse,
    Role,
    SignalingMessage,
)

app = FastAPI(title=settings.app_name)
room_manager = RoomManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/rooms", response_model=CreateRoomResponse)
def create_room(payload: CreateRoomRequest) -> CreateRoomResponse:
    room_id = uuid.uuid4().hex

    therapist_token = create_participant_token(
        room_id=room_id,
        participant_id=payload.therapist_id,
        role=Role.THERAPIST,
    )
    client_token = create_participant_token(
        room_id=room_id,
        participant_id=payload.client_id,
        role=Role.CLIENT,
    )

    return CreateRoomResponse(
        room_id=room_id,
        therapist=ParticipantTokenResponse(
            room_id=room_id,
            role=Role.THERAPIST,
            token=therapist_token,
        ),
        client=ParticipantTokenResponse(
            room_id=room_id,
            role=Role.CLIENT,
            token=client_token,
        ),
    )


@app.get("/ice-config", response_model=IceConfigResponse)
def ice_config() -> IceConfigResponse:
    return IceConfigResponse(
        ice_servers=[
            IceServer(urls=[settings.stun_url]),
            IceServer(
                urls=[settings.turn_url],
                username=settings.turn_username,
                credential=settings.turn_password,
            ),
        ]
    )


@app.websocket("/ws/{room_id}")
async def signaling_ws(websocket: WebSocket, room_id: str, token: str) -> None:
    payload = verify_token(token)
    if payload.get("room_id") != room_id:
        await websocket.close(code=4001, reason="Token room mismatch")
        return

    participant = Participant(
        participant_id=payload["participant_id"],
        role=payload["role"],
    )

    await websocket.accept()
    await room_manager.connect(room_id=room_id, participant=participant, websocket=websocket)

    try:
        await websocket.send_json({
            "type": "ready",
            "payload": {
                "participant_id": participant.participant_id,
                "role": participant.role,
                "room_size": room_manager.room_size(room_id),
            },
        })

        while True:
            raw_message = await websocket.receive_json()
            message = SignalingMessage.model_validate(raw_message)
            await room_manager.relay(
                room_id=room_id,
                sender_id=participant.participant_id,
                message={
                    "type": message.type,
                    "payload": message.payload,
                    "from": participant.participant_id,
                },
            )
    except WebSocketDisconnect:
        room_manager.disconnect(room_id=room_id, participant_id=participant.participant_id)
