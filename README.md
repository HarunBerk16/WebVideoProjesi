# WebVideoProjesi

Nunuterapi için 1:1 video görüşme MVP iskeleti.

## Özellikler (MVP)
- 1:1 görüşme (terapist + danışan)
- Çoklu eşzamanlı oda (her oda en fazla 2 katılımcı)
- Python FastAPI signaling backend
- WebRTC için STUN + TURN yapılandırması
- Next.js frontend başlangıç arayüzü

## Dizin Yapısı
- `backend/`: FastAPI signaling sunucusu
- `frontend/`: Next.js web istemcisi (başlangıç)
- `infra/`: Docker Compose ve coturn konfigürasyonu
- `docs/`: Mimari notları

## Backend Çalıştırma
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## API Uçları
- `GET /health`
- `POST /rooms`
  - örnek body:
```json
{
  "therapist_id": "therapist-001",
  "client_id": "client-001"
}
```
- `GET /ice-config`
- `WS /ws/{room_id}?token=...`

## Test
```bash
cd backend
pytest
```

## STUN/TURN
- Varsayılan STUN: Google STUN
- TURN için `infra/coturn/turnserver.conf` ve `backend/.env` güncellenmelidir.
- Production'da TURN secret ve kullanıcı bilgilerini güçlü değerlerle değiştirin.
