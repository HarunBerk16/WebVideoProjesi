from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nunuterapi Video Backend"
    environment: str = "dev"
    secret_key: str = "change-me"
    allowed_origins: str = "http://localhost:3000"
    stun_url: str = "stun:stun.l.google.com:19302"
    turn_url: str = "turn:nunuterapi.com:3478?transport=udp"
    turn_username: str = "nunu"
    turn_password: str = "nunu-turn-pass"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
