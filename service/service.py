from database import service_db
from service.admin import adminservice
from schema.service import ServiceCreate, ServiceUpdate, Service
from fastapi import HTTPException
from sqlalchemy.orm import Session
from model import ServiceT
from uuid import UUID
import uuid
import datetime


class Service:
    @staticmethod
    def get_all_services(db: Session):
        service = db.query(ServiceT).all()
        return service

    @staticmethod
    def get_service_by_id(service_id: UUID, db: Session):
        service = db.query(ServiceT).filter(ServiceT.id == str(service_id)).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service

    @staticmethod
    def create_service(service_create: ServiceCreate, admin_id: UUID, db: Session):
        admin = adminservice.get_admin_by_id(admin_id, db)
        if not admin:
            raise HTTPException(status_code=403, detail="Only admins can create services")
        service = ServiceT(id=str(uuid.uuid4()), **service_create.model_dump())
        service.admin_id = admin_id
        service.created_at = datetime.datetime.utcnow()
        db.add(service)
        db.commit()
        db.refresh(service)
        return {
            'message': 'Service Created Successfully',
            'details': service
        }

    @staticmethod
    def update_service(service_id: UUID, admin_id: UUID, service_update: ServiceUpdate, db: Session):
        admin = adminservice.get_admin_by_id(admin_id, db)
        if not admin:
            raise HTTPException(status_code=403, detail="Only admins can update services")
        service = Service.get_service_by_id(service_id, db)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        for key, value in service_update.model_dump().items():
            if value is not None:
                setattr(service, key, value)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def delete_service(service_id: UUID, admin_id: UUID, db: Session):
        admin = adminservice.get_admin_by_id(admin_id, db)
        if not admin:
            raise HTTPException(status_code=403, detail="Only admins can delete services")
        
        service = Service.get_service_by_id(db, service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        db.delete(service)
        db.commit()
        return {"detail": "Service deleted successfully"}
    
    
    
ServiceServices = Service()