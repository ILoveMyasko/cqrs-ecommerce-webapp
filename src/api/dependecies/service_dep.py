from typing import Annotated
from fastapi import Depends

from src.api.dependecies.db_dep import DBSessionDep
from src.api.dependecies.repository_dep import UserRepositoryDep
from src.services.user_service import UserService


async def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]