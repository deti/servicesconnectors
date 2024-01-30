""" Database configuration """

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///connectorsdb.sqlite3"

if os.getenv("ENVIRONMENT") == "test":
    SQLALCHEMY_DATABASE_URL = "sqlite:///testdb.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
