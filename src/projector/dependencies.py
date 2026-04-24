from typing import Annotated, AsyncIterator
from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.service import CategoryService
from src.globals.database import sessionmanager
from src.categories.repository import CategoryRepository

async def get_projector_db() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session

ProjectorDBSessionDep = Annotated[AsyncSession, Depends(get_projector_db)]

async def get_projector_category_repository(db: ProjectorDBSessionDep) -> CategoryRepository:
    return CategoryRepository(db)

CategoryRepositoryProjectorDep = Annotated[CategoryRepository, Depends(get_projector_category_repository)]

def get_projector_category_service(repo: CategoryRepositoryProjectorDep) -> CategoryService:
    return CategoryService(repository=repo)

CategoryServiceProjectorDep = Annotated[CategoryService, Depends(get_projector_category_service)]