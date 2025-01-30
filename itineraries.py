from flask_restx import Namespace, Resource, fields
from models import Itinerary
from flask_jwt_extended import jwt_required
from flask import Flask, jsonify, request
from datetime import datetime

    
    
itinerary_ns=Namespace('itinerary', description= "A namespace for Itineraries ")

Itinerary_model = itinerary_ns.model(
    'Itinerary',
    {
        
        'title': fields.String(required=True, description='The title of the itinerary.'),
        'user_id': fields.Integer(required=True, description='The id of the user who created the itinerary.'),
        'destination': fields.String(required=True, description='The destination of the itinerary.'),
        'details': fields.String(required=True, description='The details of the itinerary.'),
        'date': fields.Date(required=True, description='The date of the itinerary.')
        }
    )

@itinerary_ns.route('/itinerary')
class ItinerariesResource(Resource):
    @itinerary_ns.marshal_list_with(Itinerary_model)
    def get(self):
        
        itineraries = Itinerary.query.all()
        
        return [itinerary.to_dict() for itinerary in itineraries], 200 

    @itinerary_ns.marshal_with(Itinerary_model)
        
    @itinerary_ns.expect(Itinerary_model)
    def post(self):
        
        data=request.get_json()
        
        new_itinerary=Itinerary(
        
            title=data.get('title'),
            user_id=data.get('user_id'),
            destination=data.get('destination'),
            details=data.get('details'),
            date=data.get('date')
        )
        new_itinerary.save()
        return new_itinerary, 201 

                      
    
@itinerary_ns.route('/itinerary/<int:id>')
class ItineraryResource(Resource):
    @itinerary_ns.marshal_with(Itinerary_model)
    def get(self, id):
        itinerary = Itinerary.query.get_or_404(id)

        
        return jsonify(itinerary.to_dict())

    
    @itinerary_ns.marshal_with(Itinerary_model)
    @jwt_required()
    
    def put(self, id):
        itinerary_to_update = Itinerary.query.get_or_404(id)

        data=request.get_json()
        
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        itinerary_to_update.update(
            title=data.get('title'),
            user_id=data.get('user_id'),
            destination=data.get('destination'),
            details=data.get('details'),
            date=data.get('date')
            
            )
        return jsonify(itinerary_to_update.to_dict()), 200

    
    
        
    @itinerary_ns.marshal_with(Itinerary_model)
    @jwt_required()
    def delete(self, id):
        #current_user = get_jwt_identity()
        itinerary = Itinerary.query.get(id)
       # if not itinerary or itinerary.user_id != current_user["id"]:
            #return {"message": "Unauthorized"}, 401
        #db.session.delete(itinerary)
        #db.session.commit()
        return {"message": "Itinerary deleted successfully"}, 200

    