
import uuid
from datetime import datetime
from sqlalchemy import UUID, String, ForeignKey, BigInteger, text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.basemodel import Base
from src.categories.models import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID,primary_key=True, default=uuid.uuid7)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"), index=True)
    price_cents: Mapped[int] = mapped_column(BigInteger)
    #sku: Mapped[str] =
    description: Mapped[str | None]
    attributes: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    category:Mapped["Category"] = relationship("Category", back_populates="products")