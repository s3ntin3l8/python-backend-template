from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, populated from environment variables / a local .env.

    Extend this with your own fields; `extra="ignore"` keeps unrelated env vars
    from raising at startup.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "FastAPI Template"

    # Optional Fernet key (32 url-safe base64-encoded bytes) consumed by
    # app.core.encryption. Leave unset to store values as plaintext (dev only).
    DB_ENCRYPTION_KEY: str = ""


settings = Settings()
