from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    login: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str