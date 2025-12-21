from  fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import  Session
from schema.user import UserResponse
from schema.auth_schema import Token
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schema.user import UserLogin
from service.auths import authsrvc
from auth import access_expire
from database import engine
import model

model.Base.metadata.create_all(bind=engine)
auth_router  = APIRouter(tags=["Authentication"])

@auth_router.post("/login", response_model=Token)
def login(formdata: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    detail = authsrvc.authenticate(UserLogin(email=formdata.username, password_hash=formdata.password), db)
    if not detail:
        raise HTTPException(status_code=400, detail="Invalid Login Credentials")
    access_token = authsrvc.create_token(detail.email, detail.id, expires_delta = access_expire)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/user", response_model=UserResponse)
def get_current_user(current_user: UserResponse = Depends(authsrvc.get_current_user), db: Session = Depends(get_db)):
    return current_user