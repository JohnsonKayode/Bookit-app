from pydantic import BaseModel, Field, EmailStr
import datetime
from uuid import UUID

class UserBase(BaseModel):
    name: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="User email address")
    password_hash: str = Field(..., description="Hashed password for security")
    role: str = Field(default="user", description="User role: 'user' or 'admin'")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, description="Time the user was created")

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str = None
    email: str = None
    password: str = None
    class Config:
        orm_mode = True

class User(UserBase):
    id: UUID = Field(..., description="Unique identifier for the user")


class UserResponse(BaseModel):
    name: str = None
    email: str = None
    role: str = None

    class Config:
        from_attributes = True
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password_hash: str = Field(..., description="User password")

    class Config:
        orm_mode = True
    