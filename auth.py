import os
from dotenv  import load_dotenv
from passlib.context  import CryptContext
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_expire = int(os.getenv("EXPIRE"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_bearer = OAuth2PasswordBearer(tokenUrl="/login")