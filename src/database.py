"""Database module for PitcheRai."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, Dict, Optional

from . import models_db

Base = declarative_base()


def get_engine(database_url: str):
    """Create SQLAlchemy engine."""
    return create_engine(database_url)


def get_session_maker(engine):
    """Create session maker."""
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db(engine):
    """Initialize database tables."""
    models_db.Base.metadata.create_all(bind=engine)


# CRUD operations
class CRUDBase:
    """Base CRUD operations."""

    def __init__(self, model):
        self.model = model

    def create(self, db: Session, *, obj_in: Dict[str, Any]):
        """Create a new record."""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: str):
        """Get record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        """Get multiple records."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, *, db_obj, obj_in: Dict[str, Any]):
        """Update a record."""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: str):
        """Delete a record."""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# CRUD instances for each model
investors = CRUDBase(models_db.InvestorDB)
startups = CRUDBase(models_db.StartupDB)
email_templates = CRUDBase(models_db.EmailTemplateDB)
outreaches = CRUDBase(models_db.OutreachDB)
campaigns = CRUDBase(models_db.CampaignDB)


# Placeholder for database session
db = None
db = None
