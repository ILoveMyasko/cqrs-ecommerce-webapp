from elasticsearch import AsyncElasticsearch
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