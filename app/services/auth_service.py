"""
Authentication service for password hashing and verification
"""

from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import hashlib


def hash_password(password):
    """
    Hash a password using Werkzeug's secure hashing
    
    Args:
        password: Plain text password string
    
    Returns:
        str: Hashed password
    """
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)


def verify_password(password, password_hash):
    """
    Verify a password against its hash
    
    Args:
        password: Plain text password to verify
        password_hash: Hashed password to compare against
    
    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(password_hash, password)


def generate_session_token():
    """
    Generate a secure random session token
    
    Returns:
        str: Secure random token
    """
    return secrets.token_hex(32)


def check_admin_permission(user):
    """
    Check if user has admin privileges
    
    Args:
        user: User object
    
    Returns:
        bool: True if user is admin, False otherwise
    """
    return user is not None and user.is_admin


def validate_password_strength(password):
    """
    Validate password strength requirements
    
    Args:
        password: Password string to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, None
