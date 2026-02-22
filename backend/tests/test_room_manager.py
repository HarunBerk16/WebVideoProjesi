import pytest

from app.room_manager import Participant, RoomManager


class DummyWS:
    def __init__(self):
        self.messages = []

    async def send_json(self, message):
        self.messages.append(message)


@pytest.mark.asyncio
async def test_relay_sends_to_other_participant():
    manager = RoomManager()
    ws_therapist = DummyWS()
    ws_client = DummyWS()

    await manager.connect("room-1", Participant("t1", "therapist"), ws_therapist)
    await manager.connect("room-1", Participant("c1", "client"), ws_client)

    await manager.relay("room-1", "t1", {"type": "offer", "payload": {"sdp": "x"}})

    assert ws_therapist.messages == []
    assert ws_client.messages == [{"type": "offer", "payload": {"sdp": "x"}}]
