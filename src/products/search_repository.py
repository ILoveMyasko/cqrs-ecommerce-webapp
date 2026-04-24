from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError

from src.products.schemas import ProductElasticDocument


class ProductSearchRepository:
    def __init__(self, es_client : AsyncElasticsearch, index_name: str = "products"):
        self._es = es_client
        self.index = index_name


    async def search_by_id(self, product_id: UUID) -> ProductElasticDocument | None:
        try:
           res = await self._es.get(index=self.index, id=str(product_id))
           document = ProductElasticDocument.model_validate(res["_source"])
           return document
        except NotFoundError:
           return None

    async def search(self, query: str, limit: int = 10) -> list[ProductElasticDocument]:
        body = {
            "query":
                {"multi_match":
                     {
                        "query": query,
                        "fields":["name", "description"]
                     }
                 },
            "size": limit
        }