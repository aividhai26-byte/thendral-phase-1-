"""
Testimonial model for client testimonials
"""

from datetime import datetime
from app.models import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, CheckConstraint, Enum


class Testimonial(Base):
    """Testimonial model for client testimonials"""
    
    __tablename__ = 'testimonials'
    
    id = Column(Integer, primary_key=True)
    client_name = Column(String(100), nullable=False)
    company = Column(String(100))
    quote = Column(Text, nullable=False)
    image = Column(String(255))
    rating = Column(Integer, default=5)
    featured = Column(Boolean, default=False, index=True)
    status = Column(Enum('active', 'inactive', name='testimonial_status'), 
                   default='active', nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),
    )
    
    def __repr__(self):
        return f'<Testimonial {self.client_name}>'
    
    def to_dict(self):
        """Convert testimonial object to dictionary"""
        return {
            'id': self.id,
            'client_name': self.client_name,
            'company': self.company,
            'quote': self.quote,
            'image': self.image,
            'rating': self.rating,
            'featured': self.featured,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
