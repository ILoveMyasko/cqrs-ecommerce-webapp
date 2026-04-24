from uuid import UUID

from fastapi import HTTPException

from src.categories.models import Category
from src.categories.repository import CategoryRepository
from src.categories.schemas import CategoryCreate


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository= repository

    async def get_category_by_uuid(self, uuid: UUID) -> Category:
        category = await self.repository.get_by_uuid(uuid)
        if category is None:
            raise HTTPException(404, "Category not found")
        return category

    async def create_category(self, to_create: CategoryCreate):
        if to_create.parent_id:
            parent_category = await self.repository.get_by_uuid(to_create.parent_id)
            if parent_category is None:
                raise HTTPException(404, "Category not found")
        category_to_create = Category(**to_create.model_dump())
        created_category = await self.repository.create(category_to_create)
        return created_category