'''from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
# Load environment variables from .env
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # If python-dotenv is not installed,
    # environment variables must be provided by the system.
    pass


# Prefer DATABASE_URL if provided
DATABASE_URL = os.getenv("DATABASE_URL")

# Otherwise build DATABASE_URL from individual variables
if not DATABASE_URL:
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "raguser")
    db_password = os.getenv("DB_PASSWORD", "ragpass")
    db_name = os.getenv("DB_NAME", "ragdb")

    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{db_user}:{db_password}@"
        f"{db_host}:{db_port}/{db_name}"
    )


# Create database engine
def get_db_connection():
    """Create and return the SQLAlchemy database engine."""
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


# Database engine
engine = get_db_connection()


# Database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for SQLAlchemy models
Base = declarative_base()


# FastAPI database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

