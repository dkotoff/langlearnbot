from pydantic import BaseSettings
debug = False


class Settings(BaseSettings):
    TOKEN: str

    @property
    def DATABASE_URI(self):
        return f"sqlite:///database.sqlite3"

    class Config:
        env_file = ".env"

#обьект хранящий конфигурацию для бота
settings = Settings()