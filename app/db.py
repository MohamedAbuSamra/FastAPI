import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy.exc import ArgumentError

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None

try:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except (ValueError, ArgumentError) as e:
    print(f"Database configuration error: {e}")
    # Dummy SessionLocal that raises on use
    class DummySession:
        def __getattr__(self, name):
            raise RuntimeError("Database is not configured. Check your .env file.")
    SessionLocal = DummySession

Base = declarative_base() 