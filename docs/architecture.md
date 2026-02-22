# Nunuterapi 1:1 Video Görüşme - MVP Mimarisi

## Kapsam
- Yalnızca 1:1 görüşme (terapist + danışan)
- Aynı anda birden fazla bağımsız oda
- Kayıt, chat, takvim entegrasyonu yok (sonraki faz)
- E2EE ve ileri gizlilik özellikleri sonraki faz

## Bileşenler
1. **Next.js Frontend**
   - Odaya token ile giriş
   - WebRTC offer/answer + ICE candidate değişimi
2. **Python FastAPI Backend**
   - Oda oluşturma
   - Rol bazlı JWT üretme (therapist/client)
   - Signaling WebSocket
   - ICE yapılandırması (STUN/TURN)
3. **Coturn (TURN/STUN)**
   - NAT arkasındaki istemciler için media relay

## Neden bu tasarım?
- WebRTC medya doğrudan peer-to-peer akar, backend sadece signaling yapar.
- 1:1 modelde ilk aşamada SFU gerekmez.
- TURN ile kurumsal ağ/firewall durumlarında bağlantı başarısı artar.

## AWS Linux Yayın Planı
- EC2 Ubuntu 22.04
- Nginx reverse proxy:
  - `nunuterapi.com` -> Frontend
  - `nunuterapi.com/api` -> FastAPI
  - `nunuterapi.com/ws` -> WebSocket proxy
- TLS: Let's Encrypt
- TURN: Aynı sunucuda veya ayrı EC2 üzerinde coturn (öneri: ayrı sunucu)

## Ölçekleme Notu
- Bu MVP, 1:1 ve orta trafik için uygundur.
- Yük artarsa:
  - Backend stateless container + ALB
  - Redis ile oda/presence state paylaşımı
  - TURN sunucusu yatay ölçek
