from fastapi import HTTPException
from src.security import hash_password
from src.users.repository import UserRepository
from src.users.models import User
from src.users.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, create_dto: UserCreate) -> User:
        existing_users = await self.repository.get_by_unique_fields(
            username=create_dto.username,
            email=create_dto.email
        )
        if existing_users:
            for user in existing_users:
                if user.email == create_dto.email:
                    raise HTTPException(status_code=400, detail="Email taken")
                if user.username == create_dto.username:
                    raise HTTPException(status_code=400, detail="Username taken")

        hashed_password = hash_password(create_dto.password)
        user_to_create = User(
            email=create_dto.email,
            username=create_dto.username,
            hashed_password=hashed_password,
            is_superuser=create_dto.is_superuser)

        new_user = await self.repository.create(user_to_create)
        return new_user

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
