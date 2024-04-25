from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_HOST: str = "localhost"
    MODEL_PORT: int = 8007
    model_config = SettingsConfigDict(env_file=".env")


conf = Settings()
