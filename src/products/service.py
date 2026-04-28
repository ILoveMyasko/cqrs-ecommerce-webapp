from uuid import UUID
from fastapi import HTTPException

from src.categories.service import CategoryService
from src.products.models import Product
from src.products.repository import ProductRepository
from src.products.schemas import ProductCreate, ProductSearchParams, SearchResponse
from src.products.search_repository import ProductSearchRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository
                 , category_service: CategoryService
                 , search_repository: ProductSearchRepository):
        self.repo = product_repository
        self.category_service = category_service
        self.search_repo = search_repository

    async def create_product(self, to_create: ProductCreate):
        await self.category_service.get_category_by_uuid(to_create.category_id)
        product_to_create = Product(**to_create.model_dump())
        created_product = await self.repo.create(product_to_create)
        return created_product


    async def get_product_by_uuid(self, uuid: UUID):
        product = await self.repo.get_by_uuid(uuid)
        if product is None:
            raise HTTPException(404, "Product not found")
        return product

    async def search_products(self, params: ProductSearchParams) -> SearchResponse:
        raw_response = await self.search_repo.search(params)

        return SearchResponse(
            total=raw_response["hits"]["total"]["value"],
            items=[hit["_source"] for hit in raw_response["hits"]["hits"]],
            aggregations=raw_response.get("aggregations")
        )