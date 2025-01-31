from flask_restx import Namespace, Resource, fields
from models import Itinerary
from flask_jwt_extended import jwt_required
from flask import jsonify, request
from datetime import datetime
from exts import db

# Define the namespace
itinerary_ns = Namespace('itinerary', description="A namespace for Itineraries")

# Define the itinerary model for API documentation
Itinerary_model = itinerary_ns.model(
    'Itinerary',
    {
        'id': fields.Integer(description='The itinerary ID'),
        'title': fields.String(required=True, description='The title of the itinerary'),
        'user_id': fields.Integer(required=True, description='The ID of the user who created the itinerary'),
        'destination': fields.String(required=True, description='The destination of the itinerary'),
        'details': fields.String(required=True, description='The details of the itinerary'),
        'date': fields.String(required=True, description='The date of the itinerary (YYYY-MM-DD)')
    }
)

# Route for retrieving and creating itineraries
@itinerary_ns.route('/itinerary')
class ItinerariesResource(Resource):
    @itinerary_ns.marshal_list_with(Itinerary_model)
    def get(self):
        """Fetch all itineraries"""
        itineraries = Itinerary.query.all()
        return itineraries, 200  # No need to convert to a dict if using marshal_with

    @jwt_required()
    @itinerary_ns.expect(Itinerary_model)
    @itinerary_ns.marshal_with(Itinerary_model)
    def post(self):
        """Create a new itinerary"""
        data = request.get_json()

        # Validate input
        if not data:
            return {"error": "Invalid JSON data"}, 400
        
        # Convert date to correct format
        try:
            formatted_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

        new_itinerary = Itinerary(
            title=data.get('title'),
            user_id=data.get('user_id'),
            destination=data.get('destination'),
            details=data.get('details'),
            date=formatted_date
        )

        db.session.add(new_itinerary)
        db.session.commit()

        return new_itinerary, 201

# Route for retrieving, updating, and deleting a specific itinerary
@itinerary_ns.route('/itinerary/<int:id>')
class ItineraryResource(Resource):
    @jwt_required()
    @itinerary_ns.marshal_with(Itinerary_model)
    def get(self, id):
        """Get an itinerary by ID"""
        itinerary = Itinerary.query.get_or_404(id)
        return itinerary, 200

    @jwt_required()
    @itinerary_ns.expect(Itinerary_model)
    @itinerary_ns.marshal_with(Itinerary_model)
    def put(self, id):
        """Update an existing itinerary"""
        itinerary = Itinerary.query.get_or_404(id)
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON data"}, 400

        # Convert date format if present
        if 'date' in data:
            try:
                data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

        # Update fields
        itinerary.title = data.get('title', itinerary.title)
        itinerary.user_id = data.get('user_id', itinerary.user_id)
        itinerary.destination = data.get('destination', itinerary.destination)
        itinerary.details = data.get('details', itinerary.details)
        itinerary.date = data.get('date', itinerary.date)

        db.session.commit()
        return itinerary, 200

    @jwt_required()
    def delete(self, id):
        """Delete an itinerary"""
        itinerary = Itinerary.query.get(id)
        if not itinerary:
            return {"error": "Itinerary not found"}, 404

        db.session.delete(itinerary)
        db.session.commit()
        return {"message": "Itinerary deleted successfully"}, 200
