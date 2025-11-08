# from database import booking_db, service_db, user_db
from schema.booking import BookingBase, BookingCreate, BookingUpdate, Booking
from service.user import userservice
from service.service import ServiceServices
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from model import BookingT
import datetime



class BookingService:
    @staticmethod
    def create_booking(booking_create: BookingCreate, user_id: UUID, service_id: UUID, db: Session):
        user = userservice.get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found-booking")
        
        service = ServiceServices.get_service_by_id(service_id, db)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # booking_id = len(booking_db) + 1
        booking = BookingT(id = str(uuid.uuid4()), **booking_create.model_dump())
        booking.user_id = user_id
        booking.service_id = service_id
        booking.created_at = datetime.datetime.utcnow()
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return {
            'message': 'Booking Created Successfully',
            'details': booking
        }

    @staticmethod
    def get_all_booking(db: Session):
        booking = db.query(BookingT).all()
        return booking
    
    @staticmethod
    def get_booking_by_id(booking_id: UUID, db: Session):
        booking = db.query(BookingT).filter(BookingT.id == str(booking_id)).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    
    @staticmethod
    def get_all_bookings_by_user(user_id: UUID, db: Session):
        user = userservice.get_user_by_id(user_id, db)
        if not user:
            raise ValueError("user not found")
        
        bookings = db.query(BookingT).filter(BookingT.user_id == str(user_id)).all()
        return bookings

    @staticmethod
    # get the booking by id but only show the bookings that belong to a particular user and not all bookings
    def get_booking_by_user_id(booking_id: UUID, user_id: UUID, db: Session):
        user = userservice.get_user_by_id(user_id, db)
        if not user:
            raise ValueError("user not found")
        
        booking = BookingServices.get_booking_by_id(booking_id, db)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
            
        if booking.user_id != str(user_id):
            raise HTTPException(status_code=404, detail="This booking does not belong to this user")
        
        return booking
        
# replicate this for  admin as well.
    @staticmethod
    def update_booking(booking_id: UUID, user_id: UUID, booking_update: BookingUpdate, db: Session):
        booking = BookingServices.get_booking_by_user_id(booking_id, user_id, db)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
            
        if str(booking.user_id) != str(user_id):  # Changed from booking["user_id"] to booking.user_id
            raise HTTPException(status_code=403, detail="Booking belongs to another user - ID mismatch")
        
        for key, value in booking_update.model_dump().items():
            if value is not None:
                setattr(booking, key, value)

        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def delete_booking(booking_id: UUID, user_id: UUID, db: Session):
        user = userservice.get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        booking = BookingServices.get_booking_by_id(booking_id, db)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        db.delete(booking)
        db.commit()
        return {"detail": "Booking deleted successfully"}


BookingServices = BookingService()