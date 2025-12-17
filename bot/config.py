from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_IDS: str = ""

    # Database
    DATABASE_URL: str

    # API
    API_BASE_URL: str = "http://backend:8000"

    @property
    def admin_ids(self) -> List[int]:
        if not self.TELEGRAM_ADMIN_IDS:
            return []
        return [int(id.strip()) for id in self.TELEGRAM_ADMIN_IDS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
