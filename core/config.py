from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_NAME_TEST: str
    DB_PASS: str
    DB_PORT: int
    DB_USER: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_db_url_test(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME_TEST}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
