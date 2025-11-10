from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Boolean
import datetime
from database import Base



class UserT(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=False, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ServiceT(Base):
    __tablename__ = "service"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    duration_minutes = Column(String, nullable=False)
    is_active = Column(String, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    admin_id = Column(String, ForeignKey("user.id"), nullable=False)

class BookingT(Base):
    __tablename__ = "booking"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    service_id = Column(String, ForeignKey("service.id"), nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    status = Column(String, default="confirmed", nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)