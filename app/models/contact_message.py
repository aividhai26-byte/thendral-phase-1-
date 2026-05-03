"""
ContactMessage model for form submissions from contact page
"""

from datetime import datetime
from app.models import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime


class ContactMessage(Base):
    """ContactMessage model for form submissions from contact page"""
    
    __tablename__ = 'contact_messages'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    subject = Column(String(200))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    is_responded = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ContactMessage {self.name} - {self.subject}>'
    
    def to_dict(self):
        """Convert contact message object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'is_read': self.is_read,
            'is_responded': self.is_responded,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
