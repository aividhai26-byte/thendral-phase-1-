"""
TeamMember model for company team/staff
"""

from datetime import datetime
from app.models import Base
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime


class TeamMember(Base):
    """TeamMember model for company team/staff"""
    
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position = Column(String(100))
    image = Column(String(255))
    bio = Column(Text)
    status = Column(Enum('active', 'inactive', name='team_status'), 
                   default='active', nullable=False, index=True)
    display_order = Column(Integer, default=0, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<TeamMember {self.name} - {self.position}>'
    
    def to_dict(self):
        """Convert team member object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'image': self.image,
            'bio': self.bio,
            'status': self.status,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
