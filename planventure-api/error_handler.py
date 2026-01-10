"""
Error handling utilities and error response formatter.
"""

import logging
from flask import jsonify
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)


class ErrorResponse:
    """Format consistent error responses."""
    
    @staticmethod
    def format(message, status_code=500, field=None, details=None):
        """
        Format an error response.
        
        Args:
            message: Error message
            status_code: HTTP status code
            field: Optional field name that caused error
            details: Optional additional error details
            
        Returns:
            Tuple of (response dict, status_code)
        """
        response = {
            'error': message,
            'status_code': status_code,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if field:
            response['field'] = field
        
        if details:
            response['details'] = details
        
        return response, status_code
    
    @staticmethod
    def validation_error(message, field=None):
        """Format a 400 validation error."""
        return ErrorResponse.format(message, 400, field)
    
    @staticmethod
    def unauthorized(message="Unauthorized"):
        """Format a 401 unauthorized error."""
        return ErrorResponse.format(message, 401)
    
    @staticmethod
    def forbidden(message="Access denied"):
        """Format a 403 forbidden error."""
        return ErrorResponse.format(message, 403)
    
    @staticmethod
    def not_found(message="Resource not found"):
        """Format a 404 not found error."""
        return ErrorResponse.format(message, 404)
    
    @staticmethod
    def conflict(message="Resource already exists"):
        """Format a 409 conflict error."""
        return ErrorResponse.format(message, 409)
    
    @staticmethod
    def server_error(message="Internal server error"):
        """Format a 500 server error."""
        return ErrorResponse.format(message, 500)


def log_error(error_type, message, exception=None):
    """
    Log an error with context.
    
    Args:
        error_type: Type of error (e.g., 'ValidationError', 'DatabaseError')
        message: Error message
        exception: Optional exception object for stack trace
    """
    if exception:
        logger.error(f"{error_type}: {message}", exc_info=exception)
    else:
        logger.error(f"{error_type}: {message}")


def handle_database_error(error):
    """
    Handle database errors.
    
    Args:
        error: Database error exception
        
    Returns:
        Formatted error response
    """
    log_error("DatabaseError", str(error), error)
    return ErrorResponse.format(
        "A database error occurred. Please try again later.",
        500,
        details=str(error) if str(error) else None
    )


def handle_validation_error(error):
    """
    Handle validation errors.
    
    Args:
        error: ValidationError exception
        
    Returns:
        Formatted error response
    """
    return ErrorResponse.format(
        error.message,
        error.status_code,
        field=error.field
    )
