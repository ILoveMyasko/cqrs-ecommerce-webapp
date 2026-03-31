from typing import Annotated

from fastapi import Depends

from src.api.dependecies.db_dep import DBSessionDep
from src.crud.user_repository import UserRepository


def get_user_repository(db: DBSessionDep) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]