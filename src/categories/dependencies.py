from typing import Annotated

from fastapi import Depends

from src.globals.database import DBSessionDep
from src.categories.repository import CategoryRepository
from src.categories.service import CategoryService

def get_category_repository(db: DBSessionDep) -> CategoryRepository:
    return CategoryRepository(db)

CategoryRepositoryDep = Annotated[CategoryRepository, Depends(get_category_repository)]

def get_category_service(repo: CategoryRepositoryDep) -> CategoryService:
    return CategoryService(repository=repo)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]