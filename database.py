import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# print(SessionLocal)
print("\n 'Database session initialized' \n")

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_db = {
    "1": {
      "name": "musa table",
      "email": "string",
      "password_hash": "string",
      "role": "admin",
      "id": 1
    },

    "2": {
      "name": "Johnson",
      "email": "string",
      "password_hash": "string",
      "role": "admin",
      "id": 2
    },
    
    "3": {
      "name": "mafejopami",
      "email": "string",
      "password_hash": "string",
      "role": "admin",
      "id": 3
    },
}

service_db = {
    "1": {
    "title": "Cleaning service",
    "description": "For your laudry services",
    "price": 190,
    "duration_minutes": 2,
    "is_active": True,
    "created_at": "2025-10-01T17:41:48.930000+00:00",
    "id": 1,
    "admin_id": 1
  },
  "2": {
    "title": "TTofu service",
    "description": "For your tofu services",
    "price": 90,
    "duration_minutes": 2,
    "is_active": True,
    "created_at": "2025-10-01T17:41:48.930000+00:00",
    "id": 2,
    "admin_id": 2
  },
  "3": {
    "title": "phone repair service",
    "description": "For your phhone repair services",
    "price": 190,
    "duration_minutes": 5,
    "is_active": True,
    "created_at": "2025-10-01T17:41:48.930000+00:00",
    "id": 3,
    "admin_id": 3
  }
}

booking_db = {}

review_db = {}