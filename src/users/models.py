from sqlalchemy.orm import Mapped, mapped_column

from src.globals.basemodel import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index= True, unique=True)
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)