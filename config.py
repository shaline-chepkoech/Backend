from decouple import config
import os 
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True
        #JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='secret')
        
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # Use PostgreSQL on Render
    DEBUG = False
    
class TestConfig(Config):
        SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
        SQLALCHEMY_ECHO=False
        TESTING=True
        