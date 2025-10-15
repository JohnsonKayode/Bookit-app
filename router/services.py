from service.service import ServiceServices
from fastapi import HTTPException, APIRouter, Depends
from schema.service import ServiceCreate, ServiceUpdate, Service, ServiceBase
# from database import admin_db, service_db
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from uuid import UUID
from service.admin import adminservice

Base.metadata.create_all(bind=engine)

services_router = APIRouter()


@services_router.post("/services/{admin_id}")
async def create_service(service_create: ServiceCreate, admin_id: UUID, db: Session = Depends(get_db)):
    details = ServiceServices.create_service(service_create, admin_id, db)
    return details

@services_router.get("/services/")
async def get_all_services(db: Session = Depends(get_db)):
    details = ServiceServices.get_all_services(db)
    return details

@services_router.get("/services/{service_id}")
async def get_service_by_id(service_id: UUID, db: Session = Depends(get_db)):
    details = ServiceServices.get_service_by_id(service_id, db)
    return details

@services_router.patch("/services/{service_id}/{admin_id}")
async def update_service(service_id: UUID, admin_id: UUID, service_update: ServiceUpdate, db: Session = Depends(get_db)):
    details = ServiceServices.update_service(service_id, admin_id, service_update, db)
    return details

@services_router.delete("/services/{service_id}/{admin_id}")
async def delete_service(service_id: UUID, admin_id: UUID, db: Session = Depends(get_db)):
    details = ServiceServices.delete_service(service_id, admin_id, db)
    return details