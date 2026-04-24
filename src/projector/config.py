from pydantic_settings import BaseSettings

from src.globals.config import settings


class ProjectorSettings(BaseSettings):
    CATEGORY_TOPIC : str = "cdc.public.categories"
    PRODUCT_TOPIC: str = "cdc.public.products"
    DEBEZIUM_URL: str = "http://localhost:8083"
    CONNECTOR_NAME:str = "postgres-connector"
    GROUP_ID: str = "v7"
    DEBEZIUM_CONNECTOR_CONFIG: dict = {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "plugin.name": "pgoutput",
        "database.hostname": "postgres",
        "database.port": "5432",
        "database.user": settings.DATABASE_USER,
        "database.password": settings.DATABASE_PASSWORD,
        "database.dbname": "postgres",
        "topic.prefix": "cdc",
        "table.include.list": "public.products,public.categories",
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable": "false",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable": "false",
        "decimal.handling.mode": "double",
        "heartbeat.interval.ms": "30000",
        "time.precision.mode": "connect"
    }


projector_settings = ProjectorSettings()
