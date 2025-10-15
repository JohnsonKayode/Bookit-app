from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class AdminBase(BaseModel):
    name: str = Field(..., description="Full name of the admin")
    email: EmailStr = Field(..., description="Admin email address")
    password_hash: str = Field(..., description="Hashed password for security")
    role: str = Field(..., description="Admin role: 'admin'")

    class Config:
        orm_mode = True

class AdminCreate(AdminBase):
    pass

class AdminUpdate(BaseModel):
    name: str = None
    email: EmailStr = None
    password: str = None
    role: str = None

class Admin(AdminBase):
    id: UUID = Field(..., description="Unique identifier for the admin")