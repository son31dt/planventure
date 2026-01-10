"""
Authentication routes for user registration and login.
"""

from flask import request, jsonify
from . import auth_bp
from models import db, User
from utils import generate_token, generate_refresh_token
from exceptions import ValidationError, AuthenticationError, ConflictError, DatabaseError
from error_handler import ErrorResponse
import re
import logging

logger = logging.getLogger(__name__)


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    
    return True, ""


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON body:
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "full_name": "string" (optional)
    }
    
    Returns:
        201: User created successfully with access and refresh tokens
        400: Invalid request or validation error
        409: User already exists
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError('No data provided')
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        
        # Validate required fields
        if not username:
            raise ValidationError('Username is required', 'username')
        
        if not email:
            raise ValidationError('Email is required', 'email')
        
        if not password:
            raise ValidationError('Password is required', 'password')
        
        # Validate email format
        if not validate_email(email):
            raise ValidationError('Invalid email format', 'email')
        
        # Validate password strength
        is_valid_password, password_error = validate_password(password)
        if not is_valid_password:
            raise ValidationError(password_error, 'password')
        
        # Validate username length
        if len(username) < 3 or len(username) > 80:
            raise ValidationError('Username must be between 3 and 80 characters', 'username')
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                raise ConflictError('Username already exists')
            else:
                raise ConflictError('Email already registered')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name if full_name else None
        )
        new_user.set_password(password)
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"New user registered: {new_user.email}")
        
        # Generate tokens
        access_token = generate_token(new_user.id, new_user.email)
        refresh_token = generate_refresh_token(new_user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except (ValidationError, ConflictError) as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}", exc_info=e)
        raise DatabaseError('Registration failed. Please try again.')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user.
    
    Expected JSON body:
    {
        "email": "string",
        "password": "string"
    }
    
    Returns:
        200: Login successful with access and refresh tokens
        400: Invalid request
        401: Invalid credentials
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError('No data provided')
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            raise ValidationError('Email and password are required')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            logger.warning(f"Failed login attempt for email: {email}")
            raise AuthenticationError('Invalid email or password')
        
        if not user.is_active:
            logger.warning(f"Login attempt with inactive account: {email}")
            raise AuthenticationError('Account is inactive')
        
        logger.info(f"User logged in: {user.email}")
        
        # Generate tokens
        access_token = generate_token(user.id, user.email)
        refresh_token = generate_refresh_token(user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except (ValidationError, AuthenticationError) as e:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=e)
        raise DatabaseError('Login failed. Please try again.')


@auth_bp.route('/validate-email', methods=['POST'])
def validate_email_endpoint():
    """
    Validate email format without registration.
    
    Expected JSON body:
    {
        "email": "string"
    }
    
    Returns:
        200: Email validation result
    """
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    
    email = data.get('email', '').strip()
    is_valid = validate_email(email)
    
    # Check if email already exists
    email_exists = User.query.filter_by(email=email).first() is not None
    
    return jsonify({
        'valid': is_valid,
        'available': not email_exists if is_valid else False
    }), 200
