from typing import Annotated, AsyncIterator
from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.globals.database import sessionmanager
from src.categories.repository import CategoryRepository

async def get_projector_db() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session

ProjectorDBSessionDep = Annotated[AsyncSession, Depends(get_projector_db)]

async def get_projector_category_repository(db: ProjectorDBSessionDep) -> CategoryRepository:
    return CategoryRepository(db)

CategoryRepoDep = Annotated[CategoryRepository, Depends(get_projector_category_repository)]