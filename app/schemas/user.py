# app/schemas/user.py

from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8) # type: ignore
    username: constr(strip_whitespace=True, min_length=3, max_length=32) # type: ignore

class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
