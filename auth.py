from flask_restx import Resource, Namespace, fields
from models import User
from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (JWTManager, 
create_access_token, create_refresh_token, 
get_jwt_identity,
jwt_required)

auth_ns=Namespace('auth', description="A namespace for authentication")


signup_model = auth_ns.model(
    'Signup',
    {
        'username': fields.String(required=True, description='The username for the user.'),
        'email': fields.String(required=True, description='The email for the user.'),
        'phone_number': fields.String(required=True, description='The phone number for the user.'),
        'password': fields.String(required=True, description='The password for the user.')
    }
    )

login_model = auth_ns.model(
    'Login',
    {
        'username': fields.String(required=True, description='The username for the user.'),
        'password': fields.String(required=True, description='The password for the user.')
    }
    )

@auth_ns.route('/signup')
class Signup(Resource): 
    @auth_ns.expect(signup_model)
    def post(self):
        data=request.get_json()
        
        username=data.get('username')
        
        db_user=User.query.filter_by(username=username).first()
        
        if db_user is not None:
            return {"message":f"user with username {username} already exists"}
            
        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            password=generate_password_hash(data.get('password'))
         )
        
        new_user.save()
        
        return make_response(jsonify({"message":"user created successfully"}), 201)
        
        
        

    
@auth_ns.route('/login')
class Login(Resource):
    
    @auth_ns.expect(login_model)
    def post(self):
    
        data=request.get_json()
        
        username=data.get('username')
        password=data.get('password')
        
        db_user=User.query.filter_by(username=username).first()
        
        
        
        if db_user and check_password_hash(db_user.password, password):
            
            access_token=create_access_token(identity=db_user.username)
            refresh_token=create_refresh_token(identity=db_user.username)
            
            return jsonify(
                {"access_token": access_token, 
                "refresh_token": refresh_token}
            )
@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):   
        
        current_user=get_jwt_identity()
        
        new_access_token=create_access_token(identity=current_user)
        
        return make_response(jsonify({"access_token": new_access_token}),200) 
    
                    