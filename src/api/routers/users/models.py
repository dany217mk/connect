from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    img_url: str | None
    about: str | None

    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    name: str | None
    img_url: str | None
    about: str | None