"""
Trip management routes for CRUD operations.
All routes require JWT authentication.
"""

from flask import request, jsonify
from models import db, Trip
from middleware import user_required
from exceptions import ValidationError, NotFoundError, ConflictError, DatabaseError
from error_handler import ErrorResponse
from datetime import datetime
from utils import generate_default_itinerary
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

from . import trips_bp


@trips_bp.route('', methods=['GET'])
@user_required
def get_user_trips(user):
    """
    Get all trips for the authenticated user.
    
    Query Parameters:
        - status: Filter by trip status (planning, confirmed, completed, cancelled)
        - limit: Maximum number of results (default: 50)
        - offset: Pagination offset (default: 0)
    
    Returns:
        200: List of user's trips
    """
    try:
        status = request.args.get('status')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Base query
        query = Trip.query.filter_by(user_id=user.id)
        
        # Filter by status if provided
        if status:
            query = query.filter_by(status=status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        trips = query.order_by(Trip.start_date.desc()).limit(limit).offset(offset).all()
        
        return jsonify({
            'trips': [trip.to_dict() for trip in trips],
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve trips: {str(e)}'}), 500


@trips_bp.route('/<int:trip_id>', methods=['GET'])
@user_required
def get_trip(user, trip_id):
    """
    Get a specific trip by ID.
    Only the trip owner can view it.
    
    Returns:
        200: Trip details
        403: Access denied (not trip owner)
        404: Trip not found
    """
    try:
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        # Check ownership
        if trip.user_id != user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify(trip.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve trip: {str(e)}'}), 500


@trips_bp.route('', methods=['POST'])
@user_required
def create_trip(user):
    """
    Create a new trip.
    
    Expected JSON body:
    {
        "destination": "string",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "latitude": float (optional),
        "longitude": float (optional),
        "itinerary": object (optional),
        "notes": "string" (optional),
        "status": "string" (optional, default: planning)
    }
    
    Returns:
        201: Trip created successfully
        400: Invalid request data
        409: Trip already exists with same destination and dates
        500: Server error
    """
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError('No data provided')
        
        # Validate required fields
        destination = data.get('destination', '').strip()
        start_date_str = data.get('start_date', '').strip()
        end_date_str = data.get('end_date', '').strip()
        
        if not destination:
            raise ValidationError('Destination is required', 'destination')
        
        if not start_date_str:
            raise ValidationError('Start date is required', 'start_date')
        
        if not end_date_str:
            raise ValidationError('End date is required', 'end_date')
        
        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError('Invalid date format. Use YYYY-MM-DD', 'date')
        
        # Validate date range
        if start_date >= end_date:
            raise ValidationError('Start date must be before end date', 'dates')
        
        # Itinerary handling
        itinerary = data.get('itinerary')
        if itinerary is None:
            itinerary = generate_default_itinerary(destination, start_date, end_date)
        elif not isinstance(itinerary, dict):
            raise ValidationError('Itinerary must be an object', 'itinerary')

        # Create trip
        new_trip = Trip(
            user_id=user.id,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            itinerary=itinerary,
            notes=data.get('notes'),
            status=data.get('status', 'planning')
        )
        
        db.session.add(new_trip)
        db.session.commit()
        
        logger.info(f"Trip created by user {user.id}: {destination} ({start_date} - {end_date})")
        
        return jsonify({
            'message': 'Trip created successfully',
            'trip': new_trip.to_dict()
        }), 201
    
    except IntegrityError as e:
        db.session.rollback()
        logger.warning(f"Duplicate trip attempt by user {user.id}")
        raise ConflictError('A trip with the same destination and dates already exists')
    except (ValidationError, ConflictError) as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        logger.error(f"Trip creation error: {str(e)}", exc_info=e)
        raise DatabaseError('Failed to create trip. Please try again.')


@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@user_required
def update_trip(user, trip_id):
    """
    Update an existing trip.
    Only the trip owner can update it.
    
    Expected JSON body (all fields optional):
    {
        "destination": "string",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "latitude": float,
        "longitude": float,
        "itinerary": object,
        "notes": "string",
        "status": "string"
    }
    
    Returns:
        200: Trip updated successfully
        400: Invalid request data
        403: Access denied (not trip owner)
        404: Trip not found
    """
    try:
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        # Check ownership
        if trip.user_id != user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'destination' in data:
            destination = data['destination'].strip()
            if not destination:
                return jsonify({'error': 'Destination cannot be empty'}), 400
            trip.destination = destination
        
        if 'start_date' in data:
            try:
                trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
        
        if 'end_date' in data:
            try:
                trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400
        
        # Validate date range
        if trip.start_date >= trip.end_date:
            return jsonify({'error': 'Start date must be before end date'}), 400
        
        if 'latitude' in data:
            trip.latitude = data['latitude']
        
        if 'longitude' in data:
            trip.longitude = data['longitude']
        
        if 'itinerary' in data:
            trip.itinerary = data['itinerary']
        
        if 'notes' in data:
            trip.notes = data['notes']
        
        if 'status' in data:
            trip.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trip updated successfully',
            'trip': trip.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update trip: {str(e)}'}), 500


@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@user_required
def delete_trip(user, trip_id):
    """
    Delete a trip.
    Only the trip owner can delete it.
    
    Returns:
        200: Trip deleted successfully
        403: Access denied (not trip owner)
        404: Trip not found
    """
    try:
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        # Check ownership
        if trip.user_id != user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({'message': 'Trip deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete trip: {str(e)}'}), 500


@trips_bp.route('/upcoming', methods=['GET'])
@user_required
def get_upcoming_trips(user):
    """
    Get upcoming trips for the user (start_date >= today).
    
    Returns:
        200: List of upcoming trips
    """
    try:
        from datetime import date
        today = date.today()
        
        trips = Trip.query.filter(
            Trip.user_id == user.id,
            Trip.start_date >= today,
            Trip.status != 'cancelled'
        ).order_by(Trip.start_date.asc()).all()
        
        return jsonify({
            'trips': [trip.to_dict() for trip in trips],
            'total': len(trips)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve upcoming trips: {str(e)}'}), 500
