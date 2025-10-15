from service.booking import BookingServices
from fastapi import APIRouter, Depends, HTTPException
from schema.booking import BookingCreate, BookingUpdate, Booking
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db, engine, Base

Base.metadata.create_all(bind=engine)

booking_router = APIRouter()


@booking_router.post("/bookings/{user_id}/{service_id}")
def create_booking(booking_create: BookingCreate, user_id: UUID, service_id: UUID, db: Session = Depends(get_db)):
    new_booking = BookingServices.create_booking(booking_create, user_id, service_id, db)
    return new_booking

@booking_router.get("/bookings")
def get_all_bookings(db: Session = Depends(get_db)):
    bookings = BookingServices.get_all_booking(db)
    return bookings

@booking_router.get("/bookings/{user_id}")
def get_user_bookings(user_id: UUID, db: Session = Depends(get_db)):
    bookings = BookingServices.get_all_bookings_by_user(user_id, db)
    return bookings

@booking_router.get("/bookings/{user_id}/{booking_id}")
def get_booking_by_user_id(booking_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
    booking = BookingServices.get_booking_by_user_id(booking_id, user_id, db)
    return booking

@booking_router.get("/booking/{booking_id}")
def get_booking_by_id(booking_id: UUID, db: Session = Depends(get_db)):
    booking = BookingServices.get_booking_by_id(booking_id, db)
    return booking

@booking_router.patch("/bookings/{user_id}/{booking_id}")
def update_booking(booking_id: UUID, user_id: UUID, booking_update: BookingUpdate, db: Session = Depends(get_db)):
    updated_booking = BookingServices.update_booking(booking_id, user_id, booking_update, db)
    return updated_booking

@booking_router.delete("/bookings/{user_id}/{booking_id}")
def delete_booking(booking_id: UUID, user_id: UUID, db: Session = Depends(get_db)):  
    booking = BookingServices.delete_booking(booking_id, user_id, db)
    return booking