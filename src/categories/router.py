from fastapi import APIRouter

from src.categories.dependencies import CategoryServiceDep
from src.categories.schemas import CategoryRead, CategoryCreate

router = APIRouter(prefix="/categories")

@router.post("/", response_model=CategoryRead)
async def add_category(
        category_service: CategoryServiceDep,
        category_to_create_dto: CategoryCreate
):
    created_category = await category_service.create_category(category_to_create_dto)
    return created_category