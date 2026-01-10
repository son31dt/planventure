"""
CORS (Cross-Origin Resource Sharing) configuration utilities.
Manages allowed origins for different environments.
"""

import os
from typing import List, Dict, Any


class CORSConfig:
    """CORS configuration helper for different environments."""
    
    @staticmethod
    def get_allowed_origins() -> List[str]:
        """
        Get list of allowed CORS origins from environment.
        
        Returns:
            List of allowed origin URLs
        """
        origins_str = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173')
        # Split by comma and strip whitespace from each origin
        return [origin.strip() for origin in origins_str.split(',') if origin.strip()]
    
    @staticmethod
    def get_cors_config() -> Dict[str, Any]:
        """
        Get complete CORS configuration for Flask-CORS.
        
        Returns:
            Dictionary with CORS settings
        """
        return {
            'origins': CORSConfig.get_allowed_origins(),
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
            'allow_headers': [
                'Content-Type',
                'Authorization',
                'Accept',
                'Origin',
                'X-Requested-With'
            ],
            'expose_headers': [
                'Content-Type',
                'Authorization',
                'Content-Length',
                'X-Total-Count',
                'X-Page-Number',
                'X-Page-Size'
            ],
            'max_age': 3600,  # 1 hour
            'supports_credentials': True
        }
    
    @staticmethod
    def is_origin_allowed(origin: str) -> bool:
        """
        Check if a given origin is allowed.
        
        Args:
            origin: Origin URL to check
            
        Returns:
            True if origin is allowed, False otherwise
        """
        allowed_origins = CORSConfig.get_allowed_origins()
        return origin in allowed_origins
    
    @staticmethod
    def add_production_origins(*origins: str) -> str:
        """
        Helper to add production origins to CORS_ORIGINS env var.
        
        Args:
            *origins: One or more origin URLs to add
            
        Returns:
            Updated CORS_ORIGINS string
        """
        current = CORSConfig.get_allowed_origins()
        for origin in origins:
            if origin not in current:
                current.append(origin)
        return ','.join(current)
