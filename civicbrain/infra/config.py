"""Application configuration via pydantic-settings."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """CivicBrain system settings loaded from environment or .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "CivicBrain"
    VERSION: str = "0.14.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = "dev-secret-key-replace-in-production-with-entropy"

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/civicbrain",
        description="Async SQLAlchemy database connection string",
    )
    DATABASE_URL_SYNC: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/civicbrain",
        description="Sync database connection string for migrations/scripts",
    )
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_TIMEOUT_SECONDS: int = 10

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def assemble_async_db_url(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    # Supabase (Auth, Storage, RLS)
    SUPABASE_URL: str = "https://mock.supabase.co"
    SUPABASE_ANON_KEY: str = "mock-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: str = "mock-service-role-key"

    # Upstash Redis
    UPSTASH_REDIS_URL: str = "redis://localhost:6379"

    # Scheduled Cron Secret
    CRON_SECRET: str = "default-dev-cron-secret"

    # Frontend Base URL for Password Setup / Onboarding Links
    FRONTEND_BASE_URL: str = "http://localhost:5173/setup-password"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000,https://civicbrain.gov.in"

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def validate_cors_origins(cls, v: str) -> str:
        origins = [origin.strip() for origin in v.split(",") if origin.strip()]
        if "*" in origins:
            raise ValueError(
                "Wildcard '*' origin is forbidden in CORS_ORIGINS for production security."
            )
        return v

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
