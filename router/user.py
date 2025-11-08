from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate, User, UserResponse
from service.user import userservice
from uuid import UUID
from database import get_db, Base, engine

Base.metadata.create_all(bind=engine)

user_Router = APIRouter()

@user_Router.get("/Users-Admins")
def get_user_admins(db: Session = Depends(get_db)):
    admins = userservice.get_user_admins(db)
    return admins

@user_Router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    user = userservice.get_all_users(db)
    return user

@user_Router.get("/users/{user_id}")
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = userservice.get_user_by_id(user_id, db)
    return user

@user_Router.post("/users")
def create_user(user: UserCreate, db:Session = Depends(get_db)):
    new_user = userservice.create_user(user, db)
    return new_user

@user_Router.patch("/users/{user_id}")
def update_user(user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = userservice.update_user(user_id, user_update, db)
    return updated_user

@user_Router.delete("/users/{user_id}/{admin_id}")
def delete_user(user_id: UUID, admin_id: UUID, db: Session = Depends(get_db)):
    result = userservice.delete_user(user_id, admin_id, db)
    return result