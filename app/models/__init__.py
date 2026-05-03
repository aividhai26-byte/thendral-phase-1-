"""
SQLAlchemy Models for Thendral City Developers Website
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import get_config

# Create base class for all models
Base = declarative_base()

# Import all model classes
from app.models.user import User
from app.models.project import Project, ProjectPhoto
from app.models.service import Service
from app.models.testimonial import Testimonial
from app.models.contact_message import ContactMessage
from app.models.team_member import TeamMember
from app.models.image_gallery import ImageGallery

# List of all models for easy access
__all__ = [
    'Base',
    'User',
    'Project',
    'ProjectPhoto',
    'Service',
    'Testimonial',
    'ContactMessage',
    'TeamMember',
    'ImageGallery'
]