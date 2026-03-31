from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_superuser: bool

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id : int
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    email: str | None = None
    is_superuser: bool | None = None