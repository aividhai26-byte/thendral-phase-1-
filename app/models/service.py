"""
Service model for services offered by the company
"""

from datetime import datetime
from app.models import Base
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime


class Service(Base):
    """Service model for services offered by the company"""
    
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    image = Column(String(255))
    display_order = Column(Integer, default=0, index=True)
    status = Column(Enum('active', 'inactive', name='service_status'), 
                   default='active', nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Service {self.title}>'
    
    def to_dict(self):
        """Convert service object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'image': self.image,
            'display_order': self.display_order,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
