import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate, User, UserResponse
from model import UserT
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
    def create_user(user: UserCreate, user_db: Session) -> UserResponse:
        details = UserT(id = str(uuid.uuid4()), **user.model_dump())
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
    def delete_user(user_id: UUID, user_db: Session):
        user = userservice.get_user_by_id(user_db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_db.delete(user)
        user_db.commit()
        return {"detail": "User deleted successfully"}


userservice = UserService()