from typing import Annotated

from fastapi import Depends

from src.globals.database import DBSessionDep
from src.users.repository import UserRepository
from src.users.service import UserService


def get_user_repository(db: DBSessionDep) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repository=repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
