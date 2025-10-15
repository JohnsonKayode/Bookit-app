from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from schema.admin import AdminUpdate, Admin, AdminBase, AdminCreate
from service.admin import adminservice
from uuid import UUID
from database import get_db, Base, engine, user_db

Base.metadata.create_all(bind=engine)

admin_Router = APIRouter()


@admin_Router.get("/admins")
def get_all_admins(db: Session = Depends(get_db)):
    admins = adminservice.get_all_admins(db)
    return admins

@admin_Router.get("/admins/{admin_id}")
def get_admin_by_id(admin_id: UUID, db: Session = Depends(get_db), ):
    admin = adminservice.get_admin_by_id(admin_id, db)
    return admin

@admin_Router.patch("/admins/{admin_id}")
def update_admin(admin_id: UUID, admin_update: AdminUpdate, db: Session = Depends(get_db)):
    updated_admin = adminservice.update_admin(admin_id, admin_update, db)
    return updated_admin

@admin_Router.delete("/admins/{admin_id}")
def delete_admin(admin_id: UUID, db: Session = Depends(get_db)):
    result = adminservice.delete_admin(admin_id, db)
    return result