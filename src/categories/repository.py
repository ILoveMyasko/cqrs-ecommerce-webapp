
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.categories.models import Category

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_uuid(self, uuid: UUID) -> Category | None:
        statement = select(Category).where(Category.id == uuid)
        result = await self.session.execute(statement)
        category = result.scalar_one_or_none()
        return category


    async def create(self, new_category : Category):
        self.session.add(new_category)
        await self.session.flush()
        await self.session.refresh(new_category)
        return new_category