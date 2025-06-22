"""
This file contains the database configuration for the application.
"""

import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)


def init_db():
    """
    Initialize the database
    """
    SQLModel.metadata.create_all(engine)


def get_db():
    """
    Get a database session
    """
    db = Session(engine)
    try:
        return db
    finally:
        db.close()
