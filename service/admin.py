import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from schema.admin import AdminCreate, AdminUpdate, Admin, AdminBase
from model import UserT
# from database import get_db, user_db


class AdminService:
    @staticmethod
    def get_all_admins(db: Session):
        admin = db.query(UserT).filter(UserT.role == "admin").all()
        if not admin:
            return HTTPException(status_code=404, detail="No admins found")
        
        temp_db = {}
        for admins in admin:
            temp_db[admins.id] = admins
        return temp_db
    
    @staticmethod
    def get_admin_by_id(admin_id: UUID, db: Session):
        admin = db.query(UserT).filter(UserT.id == str(admin_id)).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        if admin.role != "admin":  # Changed from admin["role"] to admin.role
            raise HTTPException(status_code=401, detail="Not an admin")
        return admin
    
    
    @staticmethod
    def update_admin(admin_id: UUID, admin_update: AdminUpdate, db: Session):
        admin = adminservice.get_admin_by_id(admin_id, db)
        if not admin:  # Changed from user to admin
            raise HTTPException(status_code=404, detail="Admin not found")
        for key, value in admin_update.model_dump().items():
            if value is not None:
                setattr(admin, key, value)
        return admin
    
    @staticmethod
    def delete_admin(admin_id: UUID, db: Session):
        admin = adminservice.get_admin_by_id(admin_id, db)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        db.delete(admin)
        db.commit()
        return {"detail": "Admin deleted successfully"}


adminservice = AdminService()