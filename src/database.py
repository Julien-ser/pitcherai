"""Database module for PitcheRai."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def get_engine(database_url: str):
    """Create SQLAlchemy engine."""
    return create_engine(database_url)


def get_session_maker(engine):
    """Create session maker."""
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db(engine):
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
