from datetime import timedelta, datetime
from schema.user import UserCreate, UserLogin
from schema.auth_schema import Token
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,  status
from database import get_db
from model import UserT
from fastapi.security import OAuth2PasswordRequestForm
from auth import pwd_context, secret_key, algorithm,  access_expire, auth_bearer
from pydantic import EmailStr
from jose import jwt, JWTError

class AuthService:
    @staticmethod
    def authenticate(user: UserCreate, db: Session = Depends(get_db)):
        details = db.query(UserT).filter(UserT.email == user.email).first()
        if not details:
            raise HTTPException(status_code=400, detail="Incorrect Email Adddress")
        if not pwd_context.verify(user.password_hash, details.password_hash):
            raise HTTPException(status_code=400, detail ="Incorrect Password")
        return details

    @staticmethod
    def create_token(email: EmailStr, id_user: str, expires_delta: timedelta):
        encode = {"email": email, "id": id_user}
        expire = datetime.now() + timedelta(minutes=15)
        encode.update({"exp": expire})
        encoded_jwt = jwt.encode(encode, secret_key, algorithm=algorithm)
        return encoded_jwt
    
    # @staticmethod
    # def user_login(user: UserLogin, db: Session = Depends(get_db)):
    #     details = authsrvc.authenticate(user, db)
    #     if not details:
    #         raise HTTPException(status_code=400, detail="Invalid Credentials")
    #     expiration = timedelta(minutes=access_expire)
    #     access_token = authsrvc.create_token(details.email, details.id, expires_delta = expiration)
    #     return {"access_token": access_token, "token_type": "bearer"}
    

    @staticmethod
    def user_login(user: UserLogin, db: Session = Depends(get_db)):
        details = authsrvc.authenticate(user, db)
        if not details:
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        
        # Ensure access_expire is converted to timedelta
        expiration = timedelta(minutes=access_expire)
        access_token = authsrvc.create_token(details.email, details.id, expires_delta=expiration)
        
        return {"access_token": access_token, "token_type": "bearer"}


    # def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #     user = authsrvc.authenticate(UserLogin(email=form_data.username, password=form_data.password), db)
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Incorrect email or password",
    #             headers={"WWW-Authenticate": "Bearer"},
    #             )
    #     access_token_expires = timedelta(minutes=access_expire)
    #     access_token = authsrvc.create_token(user.email, user.id, expires_delta=access_token_expires)
    #     return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def get_current_user(token: str = Depends(auth_bearer), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            # print(payload)
            email: str = payload.get("email")
            user_id: str = payload.get("id")
            # print(email, user_id)
            if email is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials1")
            user = db.query(UserT).filter(UserT.id == user_id).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User no longer exists"
                )
            return user
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials2")

authsrvc = AuthService()