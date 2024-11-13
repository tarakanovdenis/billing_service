from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"


class ProjectSettings(BaseModel):
    title: str = "Billing Service"
    description: str = (
        "Here it can be found information about the endpoints"
        " and data types of the available schemes of the endpoints"
    )
    docs_url: str = "/billing/docs"
    openapi_url: str = "/billing/openapi.json"
    version: str = "0.1.0"


class AuthJWT(BaseModel):
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class DatabaseSettings(EnvSettings):
    postgres_user: str = Field(default="app")
    postgres_password: str = Field(default="123qwe")
    postgres_db: str = Field(default="billing_database")
    postgres_host: str = Field(default="billing_db")
    postgres_port: int = Field(default=5432)

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisSettings(EnvSettings):
    pass


class RabbitMQSettings(EnvSettings):
    pass


class MongoDBSettings(EnvSettings):
    mongodb_host: str = Field(default="mongodb")
    mongodb_port: int = Field(default="27017")
    mongodb_db_name: str = Field(default="billing_service_database")


class StripePaymentService(EnvSettings):
    stripe_publishable_key: str = Field(default="")
    stripe_secret_key: str = Field(default="")
    stripe_webhook_secret: str = Field(default="")
    stripe_api_version: str = Field(default="2024-10-28.acacia")


class Settings(BaseSettings):
    project_settings: ProjectSettings = ProjectSettings()
    jwt_settings: AuthJWT = AuthJWT()
    db_settings: DatabaseSettings = DatabaseSettings()
    redis_settings: RedisSettings = RedisSettings()
    rabbitmq_settings: RabbitMQSettings = RabbitMQSettings()
    mongodb_settings: MongoDBSettings = MongoDBSettings()
    stripe_payment_service: StripePaymentService = StripePaymentService()

    auth_service_domain: str = "http://auth_backend:8000"
    db_url: str = (
        f"postgresql+asyncpg://{db_settings.postgres_user}"
        f":{db_settings.postgres_password}@{db_settings.postgres_host}"
        f":{db_settings.postgres_port}/{db_settings.postgres_db}"
    )
    db_echo: bool = False


settings = Settings()
