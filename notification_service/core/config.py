from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Settings(EnvSettings):
    # RabbitMQ settings
    rabbitmq_host: str = Field(default="rabbitmq")
    rabbitmq_port: int = Field(default=5672)
    rabbitmq_username: str = Field(default="username")
    rabbitmq_password: str = Field(default="password")

    # Yandex SMTP settings
    yandex_login: str = Field(default="deniskatarakanov")
    yandex_password: str = Field(default="uysjyykkdcmsgvnj")
    yandex_smtp_host: str = Field(default="smtp.yandex.ru")
    yandex_smtp_port: int = Field(default="465")
    yandex_domain: str = "yandex.ru"

    # Gmail SMTP settings
    gmail_login: str = Field(default="tarakanov021098")
    gmail_password: str = Field(default="hspd azey fybe wpan")
    gmail_smtp_host: str = Field(default="smtp.gmail.com")
    gmail_smtp_port: int = Field(default=587)
    gmail_domain: str = "gmail.com"

    # Email Sender Address
    sender_address: str = Field(default="tarakanov021098@gmail.com")

    auth_service_domain_name: str = "http://localhost:8001"


settings = Settings()
