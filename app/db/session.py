from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./dev.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
import app.models
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)