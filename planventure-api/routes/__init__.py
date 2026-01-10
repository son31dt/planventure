from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
trips_bp = Blueprint('trips', __name__, url_prefix='/api/trips')

from . import auth
from . import trips

__all__ = ['auth_bp', 'trips_bp']
