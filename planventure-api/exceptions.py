"""
Custom exception classes for the API.
"""


class ValidationError(Exception):
    """Raised when request data validation fails."""
    def __init__(self, message, field=None, status_code=400):
        self.message = message
        self.field = field
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    def __init__(self, message, status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthorizationError(Exception):
    """Raised when user lacks required permissions."""
    def __init__(self, message, status_code=403):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(Exception):
    """Raised when a resource is not found."""
    def __init__(self, message, status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ConflictError(Exception):
    """Raised when a resource already exists."""
    def __init__(self, message, status_code=409):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseError(Exception):
    """Raised when database operations fail."""
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
