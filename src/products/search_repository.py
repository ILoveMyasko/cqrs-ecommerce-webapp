from typing import Dict, Any
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.dsl import Search, Q

from src.products.schemas import ProductElasticDocument, ProductSearchParams


class ProductSearchRepository:
    def __init__(self, es_client: AsyncElasticsearch, index_name: str = "products"):
        self._es = es_client
        self.index = index_name

    async def search_by_id(self, product_id: UUID) -> ProductElasticDocument | None:
        try:
            res = await self._es.get(index=self.index, id=str(product_id))
            document = ProductElasticDocument.model_validate(res["_source"])
            return document
        except NotFoundError:
            return None

    async def search(self, params: ProductSearchParams) -> Dict[str, Any]:
        s = Search(index=self.index)
        s = s.query(
            "multi_match",
            query=params.q,
            fields=["name^5", "brand^5", "catch_all^2", "name.translit^3", "catch_all.translit"],
            type="most_fields",
            operator="and",
            fuzziness="AUTO",
            prefix_length=2
        )
        if params.category_id:
            s = s.filter("term", category_id=str(params.category_id))

        for attr in params.attrs:
            key, val = attr.split(":", 1)
            s = s.filter(
                "nested",
                path="attributes",
                query=Q("term", **{"attributes.key": key}) &
                      Q("term", **{"attributes.value_keyword": val})
            )

        s.aggs.bucket("categories", "terms", field="category_name")

        all_attrs = s.aggs.bucket("all_attributes", "nested", path="attributes")
        keys = all_attrs.bucket("keys", "terms", field="attributes.key", size=50)
        keys.bucket("values", "terms", field="attributes.value_keyword", size=20)

        start = (params.page - 1) * params.size
        s = s[start: start + params.size]

        search_body = s.to_dict()
        response = await self._es.search(index=self.index, body=search_body)
        return response.body
