from fastapi import APIRouter

from src.products.dependencies import ProductServiceDep
from src.products.schemas import ProductRead, ProductCreate

router = APIRouter(prefix = "/products")

@router.post("/", response_model=ProductRead)
async def add_product(
        product_service: ProductServiceDep,
        product_to_create_dto: ProductCreate
):
    created_product = await product_service.create_product(product_to_create_dto)
    return created_product

