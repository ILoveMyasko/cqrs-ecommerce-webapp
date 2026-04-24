from typing import Annotated

from fastapi import Depends

from src.categories.dependencies import CategoryServiceDep
from src.globals.database import DBSessionDep
from src.globals.elastic import ESClientDep
from src.products.repository import ProductRepository
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
