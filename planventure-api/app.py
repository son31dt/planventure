from flask import Flask, jsonify
from flask_cors import CORS
from datetime import timedelta
import os
import logging
from cors_config import CORSConfig

app = Flask(__name__)

# Configure CORS for React frontend
cors_config = CORSConfig.get_cors_config()
CORS(app, resources={
    r"/api/*": cors_config
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Initialize SQLAlchemy
from models import db, User
db.init_app(app)

# Register blueprints
from routes import auth_bp, trips_bp
app.register_blueprint(auth_bp)
app.register_blueprint(trips_bp)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

# Create database tables
with app.app_context():
    db.create_all()

# Error handlers
from error_handler import ErrorResponse
from exceptions import (
    ValidationError, AuthenticationError, AuthorizationError,
    NotFoundError, ConflictError, DatabaseError
)

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle validation errors."""
    logger.warning(f"Validation error: {error.message}")
    response, status_code = ErrorResponse.format(error.message, error.status_code, error.field)
    return jsonify(response), status_code

@app.errorhandler(AuthenticationError)
def handle_auth_error(error):
    """Handle authentication errors."""
    logger.warning(f"Authentication error: {error.message}")
    response, status_code = ErrorResponse.format(error.message, error.status_code)
    return jsonify(response), status_code

@app.errorhandler(AuthorizationError)
def handle_authz_error(error):
    """Handle authorization errors."""
    logger.warning(f"Authorization error: {error.message}")
    response, status_code = ErrorResponse.format(error.message, error.status_code)
    return jsonify(response), status_code

@app.errorhandler(NotFoundError)
def handle_not_found(error):
    """Handle not found errors."""
    logger.warning(f"Not found: {error.message}")
    response, status_code = ErrorResponse.format(error.message, error.status_code)
    return jsonify(response), status_code

@app.errorhandler(ConflictError)
def handle_conflict(error):
    """Handle conflict errors."""
    logger.warning(f"Conflict: {error.message}")
    response, status_code = ErrorResponse.format(error.message, error.status_code)
    return jsonify(response), status_code

@app.errorhandler(DatabaseError)
def handle_db_error(error):
    """Handle database errors."""
    logger.error(f"Database error: {error.message}")
    response, status_code = ErrorResponse.format(error.message, error.status_code)
    return jsonify(response), status_code

@app.errorhandler(404)
def handle_404(error):
    """Handle 404 errors."""
    response, status_code = ErrorResponse.not_found("Endpoint not found")
    return jsonify(response), status_code

@app.errorhandler(500)
def handle_500(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {str(error)}", exc_info=error)
    response, status_code = ErrorResponse.server_error("An unexpected error occurred")
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)
