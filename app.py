from flask import Flask
from flask_restx import Api
from config import DevConfig
from models import User
from models import Itinerary
from exts import db
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth_ns
from itineraries import itinerary_ns

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
#app.config['JWT_SECRET_KEY'] = 'password'  

    CORS(app)

    db.init_app(app)


    migrate = Migrate(app, db)

    JWTManager(app)

    api = Api(app, doc='/docs')
    
    api.add_namespace(itinerary_ns)
    api.add_namespace(auth_ns)



    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db, 
            "Itinerary": Itinerary,
            "User": User
            }
        
    return app   
     
    
   
    
# class Itinerary(db.Model):
#     __tablename__ = "Itineraries"
    

    
#     def __init__(self, user_id, destination, date, details, budgets):
#         self.user_id = user_id
#         self.destination = destination
#         self.date = date
#         self.details = details
        #self.budgets = budgets
        
        
# class Activity(db.Model):
#     __tablename__ = "Activities"
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     itinerary_id = db.Column(db.Integer, db.ForeignKey('Itineraries.id'), nullable=False)
#     activity_name = db.Column(db.String(100), nullable=False)
#     duration = db.Column(db.String(10), nullable=False)
    
#     def __init__(self, itinerary_id, activity_name, duration):
#         self.itinerary_id = itinerary_id
#         self.activity_name = activity_name
#         self.duration = duration
        
        
# class Budget(db.Model):
#     __tablename__ = "Budgets"   
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     itinerary_id = db.Column(db.Integer, db.ForeignKey('Itineraries.id'), nullable=False)
#     activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id'), nullable=False)
#     activity_budget = db.Column(db.Float, nullable=True)
#     total_amount = db.Column(db.Float, nullable=False)
    
#     def __init__(self, itinerary_id , total_amount, activity_id, activity_budget):
#         self.itinerary_id = itinerary_id       
#         self.total_amount = total_amount
#         self.activity_id = activity_id
#         self.activity_budget = activity_budget
        
# class Notification(db.model):
#     __tablename__ = "Notifications"
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     itinerary_id = db.Column(db.Integer, db.ForeignKey('Itineraries.id'), nullable=False)
#     notification_message = db.Column(db.String(200), nullable=False)
    
    
    

