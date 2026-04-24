from uuid import UUID

from flask import session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.models import Product


class ProductRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_by_uuid(self, uuid: UUID) -> Product | None:
        statement = select(Product).where(Product.id == uuid)
        result = await self.session.execute(statement)
        product = result.scalar_one_or_none()
        return product

    async def create(self, new_product: Product):
        self.session.add(new_product)
        await self.session.flush()
        await self.session.refresh(new_product)
        return new_product