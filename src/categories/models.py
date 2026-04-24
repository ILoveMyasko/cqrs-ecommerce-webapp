import uuid
from typing import Optional
from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.globals.basemodel import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid7)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"))
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    #slug: Mapped[str]
