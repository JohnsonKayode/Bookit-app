from pydantic import BaseModel, Field, EmailStr
import datetime
from uuid import UUID

class BookingBase(BaseModel):
    start_time: str = Field(..., description="Start time of the booking in ISO 8601 format")
    end_time: str = Field(..., description="End time of the booking in ISO  8601 format")   
    status: str = Field(..., description="Status of the booking (pending | confirmed | cancelled | completed)")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, description="Time the service was created")


    class Config:
        orm_mode = True

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: str = None
    end_time: str = None   
    status: str = None

class Booking(BookingBase):
    id: UUID = Field(..., description="Unique identifier for the booking")
    user_id: UUID = Field(..., description="The id of the user who made the booking")
    service_id: UUID = Field(..., description="The id of the service being booked")
    class Config:
        orm_mode = True
        from_attributes = True