"""
Database initialization script.
Run this script to create all database tables.

Usage:
    python create_db.py
"""

from app import app, db
from models import User

def init_database():
    """Initialize the database and create all tables."""
    with app.app_context():
        # Drop all existing tables (optional - uncomment if needed)
        # db.drop_all()
        # print("Dropped all existing tables.")
        
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {', '.join(tables)}")

if __name__ == '__main__':
    init_database()
