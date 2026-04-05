import uuid

from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.basemodel import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID,primary_key=True, default=uuid.uuid7)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"), index= True)
    sku: Mapped[str] =
    description: Mapped[str | None]
