import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, Json, ConfigDict


class ProductBase(BaseModel):
    name: str
    category_id: uuid.UUID | None = None
    price_cents: int
    description: str | None = None
    attributes: dict[str, Any] | Json[dict[str, Any]]  = Field(default_factory=dict)

class ProductRead(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="ignore")

class ProductCreate(ProductBase):
    pass

class ProductElasticDocument(ProductRead):
    category_name: str | None = None