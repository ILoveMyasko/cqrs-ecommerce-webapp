from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectorSettings(BaseSettings):
    CATEGORY_TOPIC : str = "cdc.public.categories"

projector_settings = ProjectorSettings()
