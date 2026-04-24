from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    parent_id: UUID | None = None
    name: str

class CategoryRead(CategoryBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryElasticDocument(CategoryRead):
    parent_name : str | None = None

