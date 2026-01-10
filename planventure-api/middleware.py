"""
Authentication middleware and decorators for protecting routes.
"""

from functools import wraps
from flask import request, jsonify
from utils import decode_token
from models import User


def token_required(f):
    """
    Decorator to protect routes that require JWT authentication.
    Validates JWT token from Authorization header (Bearer token).
    
    Extracts user_id from token and passes it to the route.
    
    Usage:
        @app.route('/api/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'user_id': current_user['user_id']})
    
    Returns:
        401: If token is missing or invalid
        401: If token is expired
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format. Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        
        # Decode and validate token
        payload = decode_token(token)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Pass decoded payload to route
        return f(payload, *args, **kwargs)
    
    return decorated_function


def user_required(f):
    """
    Enhanced decorator that validates token and fetches the User object.
    Passes the User object to the route.
    
    Usage:
        @app.route('/api/profile')
        @user_required
        def get_profile(user):
            return jsonify({'username': user.username})
    
    Returns:
        401: If token is missing or invalid
        404: If user not found in database
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format. Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        
        # Decode token
        payload = decode_token(token)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Fetch user from database
        user = User.query.get(payload['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        # Pass user object to route
        return f(user, *args, **kwargs)
    
    return decorated_function


def optional_auth(f):
    """
    Decorator for routes that work both authenticated and unauthenticated.
    If token is provided, validates it and passes user data.
    If token is missing, passes None as current_user.
    
    Usage:
        @app.route('/api/posts')
        @optional_auth
        def get_posts(current_user):
            if current_user:
                return jsonify({'posts': 'Private'})
            return jsonify({'posts': 'Public'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = None
        
        # Try to extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
                payload = decode_token(token)
                
                if payload:
                    current_user = payload
            except (IndexError, Exception):
                pass  # Continue without auth if token is invalid
        
        # Pass current_user (None if not authenticated)
        return f(current_user, *args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """
    Decorator to protect admin-only routes.
    Validates token and checks if user is admin.
    
    Note: Requires 'is_admin' field in User model.
    
    Usage:
        @app.route('/api/admin/users')
        @admin_required
        def get_all_users(user):
            return jsonify({'users': []})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        
        # Decode token
        payload = decode_token(token)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Fetch user and check admin status
        user = User.query.get(payload['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check admin status (if is_admin field exists)
        if not hasattr(user, 'is_admin') or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        # Pass user object to route
        return f(user, *args, **kwargs)
    
    return decorated_function
