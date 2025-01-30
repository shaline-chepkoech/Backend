from exts import db
from datetime import datetime, date

class User(db.Model):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(15), unique=True)  
    password = db.Column(db.Text(), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self, username, email, phone_number):
        self.username = username
        self.email = email
        self.phone_number = phone_number        
        db.session.commit()
        
        
#Itinerary model

        
class Itinerary(db.Model):
    
    __tablename__ = "Itineraries"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(100), nullable=False)
    #budgets = db.relationship('Budget', backref='itinerary')
    date = db.Column(db.Date, nullable=True)
    
        
    def delete(self):
        db.session.delete(self)
        
    def save(self):
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        db.session.add(self)
        db.session.commit()  
        db.session.refresh(self)      
        

    def update(self, title=None, user_id=None, destination=None, details=None, date=None):
        if title:
            self.title = title
        if user_id:
            self.user_id = user_id
        if destination:
            self.destination = destination
        if details:
            self.details = details
        if date:
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d').date()
            self.date = date
        db.session.commit()
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "destination": self.destination,
            "details": self.details,
            "date": self.date.isoformat(),  
        }      
        
    def __repr__(self):
        return f'<Itinerary {self.name}>'
    
         
    
    
 
        