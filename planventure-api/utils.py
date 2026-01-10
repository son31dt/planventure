"""
Utility functions for password hashing, JWT token generation, and validation.
Uses bcrypt for secure password hashing with automatic salt generation.
Uses PyJWT for token-based authentication.
"""

import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone, date
from typing import Union, Optional, Dict, Any
from functools import wraps
from flask import request, jsonify


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with automatic salt generation.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password as a string
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.
    
    Args:
        password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    if not password or not hashed_password:
        return False
    
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def generate_salt() -> str:
    """
    Generate a new salt for password hashing.
    
    Returns:
        Base64-encoded salt string
    """
    return bcrypt.gensalt().decode('utf-8')


def hash_password_with_salt(password: str, salt: Union[str, bytes]) -> str:
    """
    Hash a password using a specific salt.
    
    Args:
        password: Plain text password to hash
        salt: Salt to use for hashing (string or bytes)
        
    Returns:
        Hashed password as a string
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    if isinstance(salt, str):
        salt = salt.encode('utf-8')
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


# JWT Token Functions

def generate_token(user_id: int, email: str, expires_in_hours: int = 24) -> str:
    """
    Generate a JWT token for user authentication.
    
    Args:
        user_id: User's unique identifier
        email: User's email address
        expires_in_hours: Token expiration time in hours (default: 24)
        
    Returns:
        JWT token as a string
    """
    secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.now(timezone.utc) + timedelta(hours=expires_in_hours),
        'iat': datetime.now(timezone.utc)
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Decoded token payload if valid, None if invalid or expired
    """
    secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_refresh_token(user_id: int, expires_in_days: int = 30) -> str:
    """
    Generate a refresh token for extended authentication.
    
    Args:
        user_id: User's unique identifier
        expires_in_days: Token expiration time in days (default: 30)
        
    Returns:
        Refresh token as a string
    """
    secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.now(timezone.utc) + timedelta(days=expires_in_days),
        'iat': datetime.now(timezone.utc)
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def token_required(f):
    """
    Decorator to protect routes that require authentication.
    Validates JWT token from Authorization header.
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'message': 'Access granted'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Decode token
        payload = decode_token(token)
        
        if payload is None:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Pass decoded user info to the route
        return f(payload, *args, **kwargs)
    
    return decorated


def extract_token_from_header() -> Optional[str]:
    """
    Extract JWT token from Authorization header.
    
    Returns:
        Token string if present, None otherwise
    """
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            return auth_header.split(' ')[1]  # Bearer <token>
        except IndexError:
            return None
    return None


# Itinerary helpers

def generate_default_itinerary(destination: str, start_date: date, end_date: date) -> Dict[str, Any]:
    """
    Generate a simple day-by-day itinerary template between two dates.

    Args:
        destination: Trip destination name
        start_date: Trip start date (datetime.date)
        end_date: Trip end date (datetime.date)

    Returns:
        Dict keyed by day_n with date and empty activities list
    """
    if not destination:
        raise ValueError("Destination is required for itinerary generation")

    if start_date is None or end_date is None:
        raise ValueError("Start and end dates are required for itinerary generation")

    if start_date > end_date:
        raise ValueError("Start date must be on or before end date")

    itinerary: Dict[str, Any] = {}
    day_index = 1
    current = start_date
    while current <= end_date:
        key = f"day_{day_index}"
        itinerary[key] = {
            "date": current.isoformat(),
            "destination": destination,
            "activities": []
        }
        day_index += 1
        current += timedelta(days=1)

    return itinerary
