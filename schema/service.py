from pydantic import BaseModel, Field
from uuid import UUID
import datetime

class ServiceBase(BaseModel):
    title: str = Field(..., description="Title of the service")
    description: str = Field(..., description="Detailed description of the service")
    price: float = Field(..., description="Price of the service")
    duration_minutes: int = Field(..., description="Duration of the service in minutes")
    is_active: bool = Field(default=True, description="Is the service active?")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, description="Time the service was created")
    class Config:
        orm_mode = True

class ServiceCreate(ServiceBase):
    pass
    class Config:
        orm_mode = True

class ServiceUpdate(BaseModel):
    title: str = None
    description: str = None
    price: float = None
    duration_minutes: int = None
    is_active: bool = None
    class Config:
        orm_mode = True

class Service(ServiceBase):
    id: UUID = Field(..., description="Unique identifier for the service")
    admin_id: UUID = Field(..., description="The id of the admin that created or made changes to the service")
    class Config:
        orm_mode = True