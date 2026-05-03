"""
Validation utilities for form inputs and file uploads
"""

import re
from werkzeug.datastructures import FileStorage
from config.config import Config


def validate_email(email):
    """
    Validate email format using regex
    
    Args:
        email: Email string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    Validate phone number format (Indian and international formats)
    
    Args:
        phone: Phone number string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's 10-15 digits
    return re.match(r'^\+?[0-9]{10,15}$', cleaned) is not None


def validate_file_extension(filename, allowed_extensions=None):
    """
    Validate file extension against allowed list
    
    Args:
        filename: Name of the file to validate
        allowed_extensions: Set of allowed extensions (default: from Config)
    
    Returns:
        bool: True if valid, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions


def validate_file_size(file_size, max_size_mb=5):
    """
    Validate file size against maximum allowed size
    
    Args:
        file_size: Size of file in bytes
        max_size_mb: Maximum size in megabytes (default: 5MB)
    
    Returns:
        bool: True if valid, False otherwise
    """
    max_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_bytes


def validate_image_file(file: FileStorage):
    """
    Comprehensive validation for image file uploads
    
    Args:
        file: FileStorage object from Flask request
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not file or not file.filename:
        return False, "No file provided"
    
    # Validate extension
    if not validate_file_extension(file.filename):
        return False, f"Invalid file type. Allowed: {', '.join(Config.ALLOWED_EXTENSIONS)}"
    
    # Validate size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Seek back to start
    
    if not validate_file_size(file_size, max_size_mb=5):
        return False, "File size exceeds 5MB limit"
    
    return True, None


def validate_project_data(data):
    """
    Validate project form data
    
    Args:
        data: Dictionary containing project data
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['title', 'category']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field.replace('_', ' ').title()} is required"
    
    if data.get('category') not in ['current', 'completed']:
        return False, "Invalid category. Must be 'current' or 'completed'"
    
    return True, None


def validate_service_data(data):
    """
    Validate service form data
    
    Args:
        data: Dictionary containing service data
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not data.get('title'):
        return False, "Title is required"
    
    return True, None


def sanitize_string(input_string, max_length=200):
    """
    Sanitize string input by removing extra whitespace and limiting length
    
    Args:
        input_string: String to sanitize
        max_length: Maximum allowed length
    
    Returns:
        str: Sanitized string
    """
    if not input_string:
        return ""
    
    # Strip leading/trailing whitespace and collapse multiple spaces
    sanitized = ' '.join(input_string.strip().split())
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized
