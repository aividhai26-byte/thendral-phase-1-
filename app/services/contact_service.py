"""
Contact Service - Business logic for contact form operations
"""

from app.models import ContactMessage
from app import db
from datetime import datetime


class ContactService:
    """Service class for contact operations"""
    
    @staticmethod
    def save_message(data):
        """
        Save contact message to database
        
        Args:
            data: Dictionary with message data (name, email, phone, subject, message)
        
        Returns:
            ContactMessage object or None if failed
        """
        try:
            message = ContactMessage(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                subject=data.get('subject'),
                message=data.get('message'),
                is_read=False,
                is_responded=False
            )
            
            db.session.add(message)
            db.session.commit()
            
            return message
            
        except Exception as e:
            db.session.rollback()
            print(f"Error saving message: {e}")
            return None
    
    @staticmethod
    def get_messages(unread_only=False, unresponded_only=False):
        """
        Get contact messages with optional filters
        
        Args:
            unread_only: Filter only unread messages
            unresponded_only: Filter only unresponded messages
        
        Returns:
            Query object for messages
        """
        query = ContactMessage.query
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        if unresponded_only:
            query = query.filter_by(is_responded=False)
        
        return query.order_by(ContactMessage.created_at.desc())
    
    @staticmethod
    def get_message(message_id):
        """
        Get single message by ID
        
        Args:
            message_id: ID of the message
        
        Returns:
            ContactMessage object or None
        """
        return ContactMessage.query.get(message_id)
    
    @staticmethod
    def mark_as_read(message_id):
        """
        Mark message as read
        
        Args:
            message_id: ID of the message
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            message = ContactMessage.query.get(message_id)
            
            if not message:
                return False
            
            message.is_read = True
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error marking message as read: {e}")
            return False
    
    @staticmethod
    def mark_as_responded(message_id):
        """
        Mark message as responded
        
        Args:
            message_id: ID of the message
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            message = ContactMessage.query.get(message_id)
            
            if not message:
                return False
            
            message.is_responded = True
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error marking message as responded: {e}")
            return False
    
    @staticmethod
    def delete_message(message_id):
        """
        Delete message
        
        Args:
            message_id: ID of the message to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            message = ContactMessage.query.get(message_id)
            
            if not message:
                return False
            
            db.session.delete(message)
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting message: {e}")
            return False
    
    @staticmethod
    def send_email(to, subject, body):
        """
        Send email notification (placeholder for actual email implementation)
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from flask import current_app
            from flask_mail import Mail, Message
            
            mail = Mail(current_app)
            
            msg = Message(
                subject=subject,
                recipients=[to],
                body=body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            
            mail.send(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    @staticmethod
    def notify_new_message(message):
        """
        Send notification for new contact message
        
        Args:
            message: ContactMessage object
        
        Returns:
            bool: True if successful, False otherwise
        """
        subject = f"New Contact Message from {message.name}"
        body = f"""
        Name: {message.name}
        Email: {message.email}
        Phone: {message.phone or 'Not provided'}
        Subject: {message.subject or 'No subject'}
        
        Message:
        {message.message}
        
        Sent at: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # Send to admin email
        from flask import current_app
        admin_email = current_app.config.get('MAIL_DEFAULT_SENDER')
        
        if admin_email:
            return ContactService.send_email(admin_email, subject, body)
        
        return True  # Return True even if email is not configured
