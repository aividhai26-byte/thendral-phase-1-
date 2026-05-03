"""
Project model for construction projects
"""

from datetime import datetime, date
from app.models import Base
from sqlalchemy import Column, Integer, String, Text, Date, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Project(Base):
    """Project model for construction projects (current and completed)"""
    
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    short_description = Column(String(500))          # for card preview
    description = Column(Text)                        # full detail
    category = Column(Enum('current', 'completed', name='project_category'), 
                      nullable=False, default='current', index=True)
    client = Column(String(100))
    location = Column(String(200))
    area_sqft = Column(String(50))                    # e.g. "2,400 sq.ft"
    floors = Column(String(20))                       # e.g. "G+3"
    project_type = Column(String(100))                # e.g. "Residential Villa"
    start_date = Column(Date)
    completion_date = Column(Date)
    image = Column(String(255))                       # main thumbnail
    youtube_url = Column(String(500))                 # YouTube embed URL
    status = Column(Enum('active', 'inactive', name='project_status'), 
                   default='active', nullable=False, index=True)
    display_order = Column(Integer, default=0, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to photos
    photos = relationship('ProjectPhoto', backref='project', cascade='all, delete-orphan',
                         order_by='ProjectPhoto.display_order')
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    def get_youtube_embed_id(self):
        """Extract YouTube video ID from URL for embedding"""
        if not self.youtube_url:
            return None
        url = self.youtube_url
        # Handle youtu.be/ID format
        if 'youtu.be/' in url:
            vid_id = url.split('youtu.be/')[-1].split('?')[0]
            return vid_id
        # Handle youtube.com/watch?v=ID format
        if 'v=' in url:
            vid_id = url.split('v=')[-1].split('&')[0]
            return vid_id
        return None
    
    def to_dict(self):
        """Convert project object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'short_description': self.short_description,
            'description': self.description,
            'category': self.category,
            'client': self.client,
            'location': self.location,
            'area_sqft': self.area_sqft,
            'floors': self.floors,
            'project_type': self.project_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'image': self.image,
            'youtube_url': self.youtube_url,
            'youtube_embed_id': self.get_youtube_embed_id(),
            'status': self.status,
            'display_order': self.display_order,
            'photos': [p.to_dict() for p in self.photos],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ProjectPhoto(Base):
    """Photos for a project — up to 6 per project"""
    
    __tablename__ = 'project_photos'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    caption = Column(String(300))
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ProjectPhoto {self.filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'caption': self.caption,
            'display_order': self.display_order,
        }
