""" Dependencies for FastAPI """

from src.database import SessionLocal


def get_db():
    """get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
