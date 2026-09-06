"""Database connection and initialization module for SQLite."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "qa_database.db")
DATABASE_URL = f"sqlite:///{DB_NAME}"

Base = declarative_base()

# Initialize Engine and Session
try:
    # `check_same_thread=False` is needed for SQLite in FastAPI
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"[DB Error] Failed to create database engine: {e}")
    engine = None
    SessionLocal = None

def get_db():
    """FastAPI dependency for database sessions."""
    if SessionLocal is None:
        raise RuntimeError("Database connection is not available.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    if engine is not None:
        import src.db.models  # Ensure models are loaded
        Base.metadata.create_all(bind=engine)
        print("[DB] All tables initialized successfully in SQLite.")
