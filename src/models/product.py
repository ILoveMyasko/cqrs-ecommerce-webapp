from sqlalchemy.orm import Mapped, mapped_column

from src.models.basemodel import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index = True, nullable=False)
    description: Mapped[str | None]
