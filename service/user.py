import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate, User, UserResponse
from model import UserT, BookingT
from service.admin import adminservice
from auth  import pwd_context
import uuid
# from database import get_db, user_db, admin_db, Base


class UserService:
    @staticmethod
    def get_user_admins(user_db: Session):
        user = user_db.query(UserT).all()
        return user

    @staticmethod
    def get_all_users(user_db: Session):
        users = user_db.query(UserT).filter(UserT.role == "user").all()
        return users

    
    @staticmethod
    def get_user_by_id(user_id: UUID, user_db: Session):
        user = user_db.query(UserT).filter(UserT.id == str(user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    @staticmethod
    def create_user(user: UserCreate, user_db: Session):
        old_user  = user_db.query(UserT).filter(UserT.email  == user.email).first()
        if old_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        details = UserT(id = str(uuid.uuid4()), **user.model_dump(exclude="password_hash"), password_hash = pwd_context.hash(user.password_hash))
        details.created_at = datetime.datetime.utcnow()  # Added created_at field
        user_db.add(details)
        user_db.commit()
        user_db.refresh(details)
        return {
            'message': 'User Created Successfully',
            'details': UserResponse.from_orm(details)
        }

    
    @staticmethod
    def update_user(user_id: UUID, user_update: UserUpdate, user_db: Session) -> UserResponse:
        user = user_db.query(UserT).filter(UserT.id  == str(user_id)).first()
        # user_dets = userservice.get_user_by_id(user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user_update.model_dump().items():
            if value is not None:
                setattr(user, key, value)
        user_db.commit()
        user_db.refresh(user)
        return {
            'message': 'User Updated Successfully',
            'details': UserResponse.from_orm(user)
        }
    
    @staticmethod
    def delete_user(user_id: UUID, admin_id: UUID, user_db: Session):
        user = userservice.get_user_by_id(user_id, user_db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        admin = adminservice.get_admin_by_id(admin_id, user_db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        if admin.role != "admin":
            raise HTTPException(status_code=401, detail="Not an admin")
        
        user_db.query(BookingT).filter(BookingT.user_id == str(user_id)).delete()
        user_db.commit()

        # user_db.query(UserT).filter(UserT.id == str(user_id)).delete()
        # user_db.commit()
        
        user_db.delete(user)
        user_db.commit()
        return {"detail": "User deleted successfully"}


userservice = UserService()