from typing import Any

from fastapi import Query
from pydantic import BaseModel, Field


class PaginationAwareRequest(BaseModel):
    limit: int = Query(100, ge=1)
    offset: int = Query(0, ge=0)


class Pagination[T](BaseModel):
    limit: int = 100
    offset: int = 0
    count: int = 0
    total: int = 0
    items: list[T] = Field(default_factory=list)

    def __init__(self, **data: Any) -> None:
        data.setdefault("count", len(data.get("items", [])))
        super().__init__(**data)
