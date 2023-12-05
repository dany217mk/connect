from typing import Optional

from pydantic import BaseModel


class PostAdd(BaseModel):
    title: str
    text: str
    images: list[str] | None


class PostResponse(BaseModel):
    id: int
    title: str
    text: str
    images: Optional[list[str]] = None
    user_id: int


class PostsListResponse(BaseModel):
    count: int
    items: list[PostResponse]