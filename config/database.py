"""
Database connection and initialization module
Provides database connection setup for SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from config.config import get_config


def get_db_engine():
    """
    Create and return SQLAlchemy engine with connection pooling
    
    Returns:
        SQLAlchemy engine instance
    """
    config = get_config()
    
    engine = create_engine(
        config.SQLALCHEMY_DATABASE_URI,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=config.SQLALCHEMY_ECHO
    )
    
    return engine


def get_db_session(engine=None):
    """
    Create and return a database session
    
    Args:
        engine: Optional SQLAlchemy engine. If not provided, creates new one.
    
    Returns:
        SQLAlchemy session instance
    """
    if engine is None:
        engine = get_db_engine()
    
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal()


def init_database(engine=None):
    """
    Initialize database by creating all tables
    
    Args:
        engine: Optional SQLAlchemy engine. If not provided, creates new one.
    """
    if engine is None:
        engine = get_db_engine()
    
    # Import all models to ensure they are registered with SQLAlchemy
    from app.models import User, Project, Service, Testimonial
    from app.models import ContactMessage, TeamMember, ImageGallery
    
    # Create all tables
    from app.models import Base
    Base.metadata.create_all(bind=engine)
