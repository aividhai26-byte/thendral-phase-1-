"""
ImageGallery model for uploaded images management
"""

from datetime import datetime
from app.models import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey


class ImageGallery(Base):
    """ImageGallery model for uploaded images management"""
    
    __tablename__ = 'image_gallery'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(50))
    related_to = Column(Enum('project', 'service', 'team', 'general', name='image_related'), 
                       default='general', nullable=False)
    related_id = Column(Integer, nullable=True)
    uploaded_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ImageGallery {self.filename}>'
    
    def to_dict(self):
        """Convert image gallery object to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'related_to': self.related_to,
            'related_id': self.related_id,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
