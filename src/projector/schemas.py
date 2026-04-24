import uuid

from pydantic import BaseModel, ConfigDict
from typing import Optional, Generic, TypeVar, Literal, List

T = TypeVar("T")


class DebeziumPayload(BaseModel, Generic[T]):
    op: Literal["c", "u", "d", "r"]
    before: Optional[DebeziumBefore] = None
    after: Optional[T] = None
    source: dict

    model_config = ConfigDict(from_attributes=True)


class DebeziumBefore(BaseModel):
    id: uuid.UUID
    name : Optional[str]
    model_config = ConfigDict(extra="ignore")