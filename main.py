from fastapi import FastAPI
from router.user import user_Router
from router.admin import admin_Router
from router.services import services_router
from router.booking import booking_router
from router.auth import auth_router

app = FastAPI()

include_router = app.include_router(user_Router)
include_router = app.include_router(admin_Router)
include_router = app.include_router(services_router)
include_router = app.include_router(booking_router)
include_router = app.include_router(auth_router)



@app.get("/")
def main_root():
    return {"message": "Welcome to Bookit app!"}