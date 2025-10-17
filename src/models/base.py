"""
This module defines the base class for all SQLAlchemy ORM models.

The `Base` object should be used as the base class when declaring new models.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
