from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    echo_sql: bool = True
    KAFKA_URL: str = "localhost:9092"
    ELASTIC_URL: str = "localhost:9200"
    model_config = SettingsConfigDict(
        env_file=".env",
    )

settings = Settings()