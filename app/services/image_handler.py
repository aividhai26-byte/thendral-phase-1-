"""
Image Handler Service - Image upload, validation, and management
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app
from app.utils.validators import validate_file_extension, validate_file_size
from app.models import ImageGallery
from app import db


class ImageHandler:
    """Service class for handling image operations"""
    
    @staticmethod
    def save_image(file, related_to='general', related_id=None, uploaded_by=None):
        """
        Save uploaded image to disk and database
        
        Args:
            file: FileStorage object from Flask request
            related_to: Entity type the image is related to
            related_id: ID of the related entity
            uploaded_by: User ID who uploaded the image
        
        Returns:
            ImageGallery object or None if failed
        """
        if not file or not file.filename:
            return None
        
        # Validate file
        if not validate_file_extension(file.filename):
            raise ValueError('Invalid file extension')
        
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if not validate_file_size(file_size, max_size_mb=5):
            raise ValueError('File size exceeds 5MB limit')
        
        # Secure filename
        filename = secure_filename(file.filename)
        
        # Add timestamp to make filename unique
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        # Save to disk
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Save to database
        image = ImageGallery(
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            related_to=related_to,
            related_id=related_id,
            uploaded_by=uploaded_by
        )
        
        db.session.add(image)
        db.session.commit()
        
        return image
    
    @staticmethod
    def delete_image(image_id):
        """
        Delete image from disk and database
        
        Args:
            image_id: ID of the image to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        image = ImageGallery.query.get(image_id)
        
        if not image:
            return False
        
        try:
            # Delete from disk
            if os.path.exists(image.file_path):
                os.remove(image.file_path)
            
            # Delete from database
            db.session.delete(image)
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting image: {e}")
            return False
    
    @staticmethod
    def validate_image(file):
        """
        Validate image file
        
        Args:
            file: FileStorage object
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not file or not file.filename:
            return False, "No file provided"
        
        if not validate_file_extension(file.filename):
            return False, "Invalid file type. Allowed: jpg, png, jpeg, gif, webp"
        
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if not validate_file_size(file_size, max_size_mb=5):
            return False, "File size exceeds 5MB limit"
        
        return True, None
    
    @staticmethod
    def generate_thumbnail(image_path, size=(200, 200)):
        """
        Generate thumbnail for image
        
        Args:
            image_path: Path to the original image
            size: Tuple of (width, height) for thumbnail
        
        Returns:
            Path to thumbnail or None if failed
        """
        try:
            from PIL import Image as PILImage
            
            img = PILImage.open(image_path)
            img.thumbnail(size)
            
            # Create thumbnail filename
            base, ext = os.path.splitext(image_path)
            thumbnail_path = f"{base}_thumb{ext}"
            
            img.save(thumbnail_path)
            
            return thumbnail_path
            
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
    
    @staticmethod
    def get_image_url(image_id):
        """
        Get public URL for image
        
        Args:
            image_id: ID of the image
        
        Returns:
            str: URL to access the image or None
        """
        image = ImageGallery.query.get(image_id)
        
        if not image:
            return None
        
        # In production, this would return a CDN URL
        # For now, return the file path relative to uploads
        return f"/uploads/{image.filename}"
    
    @staticmethod
    def get_images_by_related(related_to, related_id):
        """
        Get all images related to a specific entity
        
        Args:
            related_to: Entity type
            related_id: Entity ID
        
        Returns:
            List of ImageGallery objects
        """
        return ImageGallery.query.filter_by(
            related_to=related_to,
            related_id=related_id
        ).order_by(ImageGallery.created_at.desc()).all()
