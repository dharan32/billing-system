import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@127.0.0.1:5432/billing_db")
# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False  # Set True only for debugging SQL queries
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()


# Dependency to get DB session (FastAPI standard)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
