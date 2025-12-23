from fastapi import HTTPException, APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate, User, UserResponse
from service.auths import authsrvc
from service.user import userservice
from uuid import UUID
from database import get_db, Base, engine

Base.metadata.create_all(bind=engine)

user_Router = APIRouter(tags=["Users"])

@user_Router.get("/Users-Admins")
def get_user_admins(db: Session = Depends(get_db), user:  User = Depends(authsrvc.get_current_user)):
    admins = userservice.get_user_admins(db)
    return admins

@user_Router.get("/users")
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(authsrvc.get_current_user)):
    user = userservice.get_all_users(db)
    return user

@user_Router.get("/me/user")
def get_user_by_id(db: Session = Depends(get_db), current_user: User = Depends(authsrvc.get_current_user)):
    user = userservice.get_user_by_id(current_user.id, db)
    return user

@user_Router.post("/user")
def create_user(user: UserCreate, db:Session = Depends(get_db)):
    new_user = userservice.create_user(user, db)
    return new_user

@user_Router.patch("/users/update")
def update_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(authsrvc.get_current_user)):
    updated_user = userservice.update_user(current_user.id, user_update, db)
    return updated_user
