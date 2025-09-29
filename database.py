# kmrl-backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB for hackathon speed (file will be created as database.db)
DATABASE_URL = "sqlite:///./database.db"

# For sqlite we need connect_args to allow multithreaded access from FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Each request will get a Session from SessionLocal()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit
Base = declarative_base()