from fastapi import HTTPException
from src.globals.security import hash_password
from src.users.repository import UserRepository
from src.users.models import User
from src.users.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, to_create: UserCreate) -> User:
        existing_users = await self.repository.get_by_unique_fields(
            username=to_create.username,
            email=str(to_create.email)
        )
        if existing_users:
            for user in existing_users:
                if user.email == to_create.email:
                    raise HTTPException(status_code=400, detail="Email taken")
                if user.username == to_create.username:
                    raise HTTPException(status_code=400, detail="Username taken")

        hashed_password = hash_password(to_create.password)
        user_to_create = User(
            email=str(to_create.email),
            username=to_create.username,
            hashed_password=hashed_password,
            is_superuser=to_create.is_superuser,)

        created_user = await self.repository.create(user_to_create)
        return created_user

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(404, "User not found")
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repository.get_by_email(email)
        if user is None:
            raise HTTPException(404, "User not found")
        return user
