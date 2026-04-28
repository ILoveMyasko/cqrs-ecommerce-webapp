import uuid
from datetime import datetime
from typing import Any, Optional, List, Dict

from pydantic import BaseModel, Field, Json, ConfigDict, field_validator


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


class ProductSearchParams(BaseModel):
    q: str = Field(..., min_length=1)
    category_id: Optional[uuid.UUID] = None
    page: int = Field(1, ge=1)
    size: int = Field(24, ge=1, le=100)
    attrs: List[str] = Field(default_factory=list)

    @field_validator("attrs")
    def validate_attrs(cls, v):
        for item in v:
            if ":" not in item:
                raise ValueError(f"Атрибут '{item}' должен быть в формате key:value")
        return v

class SearchResponse(BaseModel):
    total: int
    items: List[Dict[str, Any]]
    aggregations: Optional[Dict[str, Any]]

