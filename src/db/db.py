"""
This module is responsible for initializing the database engine,
creating the database schema, and instantiating service classes.

It provides utility functions for creating a new database session
and accessing available service instances.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
# from src.models.base import Base
from src.services import ListService, SettingsService

engine = create_engine('sqlite:///movies.db', echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    """
    Creates and returns a new SQLAlchemy session.

    Returns:
        Session: A new session instance for database interaction.
    """
    return SessionLocal()

def create_services():
    """
    Instantiates and returns all available service classes.

    Returns:
        dict: A dictionary containing service instances.
    """
    session = get_session()
    list_service = ListService(session)
    settings_service = SettingsService(session)

    return {
        'list_service': list_service,
        'settings_service': settings_service,
    }
