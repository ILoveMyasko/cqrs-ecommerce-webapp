import uuid
from datetime import datetime
from typing import Any, Optional, List

from pydantic import BaseModel, Field, Json, ConfigDict


class ProductBase(BaseModel):
    name: str
    category_id: uuid.UUID # | None?
    brand: Optional[str]  = None
    price_cents: int
    description: Optional[str] = None
    attributes: dict[str, Any] | Json[dict[str, Any]]  = Field(default_factory=dict)

class ProductRead(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(extra="ignore")

class ProductCreate(ProductBase):
    pass

class AttributeNested(BaseModel):
    key: str
    value_keyword: str
    value_number: Optional[float] = None

class ProductElasticDocument(ProductRead):
    attributes: List[AttributeNested] = Field(default_factory=list)
    category_name: str
    catch_all: str


