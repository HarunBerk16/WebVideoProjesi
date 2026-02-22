from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from fastapi import WebSocket


@dataclass(frozen=True)
class Participant:
    participant_id: str
    role: str


class RoomManager:
    def __init__(self) -> None:
        self._connections: dict[str, dict[str, WebSocket]] = defaultdict(dict)
        self._participants: dict[str, dict[str, Participant]] = defaultdict(dict)

    async def connect(self, room_id: str, participant: Participant, websocket: WebSocket) -> None:
        room_connections = self._connections[room_id]
        if len(room_connections) >= 2 and participant.participant_id not in room_connections:
            await websocket.close(code=4002, reason="Room is full")
            return

        self._participants[room_id][participant.participant_id] = participant
        room_connections[participant.participant_id] = websocket

    def disconnect(self, room_id: str, participant_id: str) -> None:
        self._connections[room_id].pop(participant_id, None)
        self._participants[room_id].pop(participant_id, None)

        if not self._connections[room_id]:
            self._connections.pop(room_id, None)
            self._participants.pop(room_id, None)

    async def relay(self, room_id: str, sender_id: str, message: dict) -> None:
        for participant_id, ws in self._connections[room_id].items():
            if participant_id == sender_id:
                continue
            await ws.send_json(message)

    def room_size(self, room_id: str) -> int:
        return len(self._connections.get(room_id, {}))
