from service.booking import BookingServices
from fastapi import APIRouter, Depends, HTTPException
from schema.booking import BookingCreate, BookingUpdate, Booking
from schema.user import User
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db, engine, Base
from service.auths import authsrvc
from router.auth import get_current_user

Base.metadata.create_all(bind=engine)

booking_router = APIRouter(tags=["Booking"])


@booking_router.post("/bookings/{service_id}")
def create_booking(booking_create: BookingCreate, service_id: UUID, db: Session = Depends(get_db), current_user: list = Depends(authsrvc.get_current_user)):
    new_booking = BookingServices.create_booking(booking_create, current_user.id, service_id, db)
    return new_booking

@booking_router.get("/bookings/all")
def get_all_bookings(db: Session = Depends(get_db), current_user: User = Depends(authsrvc.get_current_user)):
    bookings = BookingServices.get_all_booking(db)
    return bookings

@booking_router.get("/bookings/{user_id}")
def get_user_bookings(db: Session = Depends(get_db), current_user: User = Depends(authsrvc.get_current_user)):
    bookings = BookingServices.get_all_bookings_by_user(current_user.id, db)
    return bookings

@booking_router.get("/bookings")
def get_my_bookings(db: Session = Depends(get_db), current_user: User = Depends(authsrvc.get_current_user)):
    bookings = BookingServices.get_my_bookings(current_user.id, db)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this user")
    return bookings

# @booking_router.get("/bookings/{user_id}/{booking_id}")
# def get_booking_by_user_id(booking_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
#     booking = BookingServices.get_booking_by_user_id(booking_id, user_id, db)
#     return booking

@booking_router.get("/booking/{booking_id}")
def get_booking_by_id(booking_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(authsrvc.get_current_user)):
    booking = BookingServices.get_booking_by_id(booking_id, db)
    return booking

@booking_router.patch("/bookings/{user_id}/{booking_id}")
def update_booking(booking_id: UUID, booking_update: BookingUpdate, db: Session = Depends(get_db),  current_user: User = Depends(authsrvc.get_current_user)):
    updated_booking = BookingServices.update_booking(booking_id, current_user.id, booking_update, db)
    return updated_booking

@booking_router.delete("/bookings/{user_id}/{booking_id}")
def delete_booking(booking_id: UUID, user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(authsrvc.get_current_user)):  
    booking = BookingServices.delete_booking(booking_id, current_user.id, db)
    return booking