from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from schema.admin import AdminUpdate, Admin, AdminBase, AdminCreate
from service.admin import adminservice
from service.user import userservice
from uuid import UUID
from database import get_db, Base, engine
from schema.user import UserResponse
from service.auths import authsrvc

Base.metadata.create_all(bind=engine)

admin_Router = APIRouter(tags=["Admins"])


@admin_Router.get("/admins")
def get_all_admins(db: Session = Depends(get_db), current_user: UserResponse = Depends(authsrvc.get_current_user)):
    admins = adminservice.get_all_admins(db)
    return admins

@admin_Router.get("/admins/{admin_id}")
def get_admin_by_id(db: Session = Depends(get_db), current_user: UserResponse = Depends(authsrvc.get_current_user)):
    admin = adminservice.get_admin_by_id(current_user.id, db)
    return admin

@admin_Router.patch("/admins/{admin_id}")
def update_admin(admin_update: AdminUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(authsrvc.get_current_user)):
    updated_admin = adminservice.update_admin(current_user.id, admin_update, db)
    return updated_admin

@admin_Router.delete("/admins/{admin_id}")
def delete_admin(admin_id: UUID, db: Session = Depends(get_db), current_user: UserResponse = Depends(authsrvc.get_current_user)):
    result = adminservice.delete_admin(admin_id, db)
    return result

@admin_Router.delete("/users/{user_id}/{admin_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db), current_user: UserResponse = Depends(authsrvc.get_current_user)):
    result = userservice.delete_user(user_id, current_user.id, db)
    return result