from dotenv import load_dotenv
from os import getenv

load_dotenv()

class DBSettings:
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class TGBotSettings:
    BOT_TOKEN = getenv("BOT_TOKEN")
    BASE_SITE = getenv("BASE_SITE")
    ADMIN_ID = getenv("ADMIN_ID")

    def get_webhook_url(self) -> str:
        return f"{self.BASE_SITE}/webhook"


db_settings = DBSettings()
bot_settings = TGBotSettings()