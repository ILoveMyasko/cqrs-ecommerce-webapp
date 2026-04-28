from typing import Annotated, Optional, List
from uuid import UUID

from fastapi import Depends, Query

from src.categories.dependencies import CategoryServiceDep
from src.globals.database import DBSessionDep
from src.globals.elastic import ESClientDep
from src.products.repository import ProductRepository
from src.products.schemas import ProductSearchParams
from src.products.search_repository import ProductSearchRepository
from src.products.service import ProductService


def get_product_repository(session_dep: DBSessionDep)->ProductRepository:
    return ProductRepository(db_session=session_dep)

ProductRepositoryDep = Annotated[ProductRepository, Depends(get_product_repository)]

def get_product_search_repository(es_client: ESClientDep)->ProductSearchRepository:
    return ProductSearchRepository(es_client)

ProductSearchRepositoryDep = Annotated[ProductSearchRepository, Depends(get_product_search_repository)]

def get_product_service(product_repository: ProductRepositoryDep
                        , category_service_dep : CategoryServiceDep
                        , product_search_repository: ProductSearchRepositoryDep
                        ) ->ProductService:
    return ProductService(product_repository=product_repository
                          , category_service= category_service_dep
                          , search_repository=product_search_repository)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


def get_search_params(
    q: str = Query(...),
    category_id: Optional[UUID] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(24, ge=1),
    attrs: List[str] = Query(default_factory=list)
) -> ProductSearchParams:
    return ProductSearchParams(
        q=q, category_id=category_id, page=page, size=size, attrs=attrs
    )

SearchParamsDep = Annotated[ProductSearchParams, Depends(get_search_params)]