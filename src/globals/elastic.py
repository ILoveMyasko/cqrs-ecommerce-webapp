from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.globals.config import settings

class ElasticManager:
    def __init__(self):
        self.client: AsyncElasticsearch | None = None

    def connect(self):
        self.client = AsyncElasticsearch(hosts=[settings.ELASTIC_URL])

    async def close(self):
        if self.client:
            await self.client.close()

es_manager = ElasticManager()

async def get_es_client() -> AsyncElasticsearch:
    return es_manager.client

ESClientDep = Annotated[AsyncElasticsearch, Depends(get_es_client)]