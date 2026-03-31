from operator import or_

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.base import state_str

from src.models.user import User


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user


    async def get_by_email(self, email:str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user


    async def get_by_username(self, username:str) -> User | None:
        statement = select(User).where(User.username==username)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user


    async def get_by_unique_fields(self, username:str, email:str):
        statement = select(User).where(
            or_(
                User.email == email,
                User.username == username
            )
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, new_user: User):
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user