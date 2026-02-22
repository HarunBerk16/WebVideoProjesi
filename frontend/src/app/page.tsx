export default function Home() {
  return (
    <main style={{ fontFamily: 'sans-serif', maxWidth: 900, margin: '40px auto' }}>
      <h1>Nunuterapi 1:1 Görüşme MVP</h1>
      <p>
        Bu arayüz başlangıç sürümüdür. Terapist ve danışan, backend tarafından üretilen token
        ile odaya bağlanır ve WebRTC eşleşmesini signaling websocket üzerinden tamamlar.
      </p>
      <ul>
        <li>Rol bazlı: therapist / client</li>
        <li>1:1 oda limiti</li>
        <li>STUN + TURN desteği</li>
      </ul>
    </main>
  );
}
