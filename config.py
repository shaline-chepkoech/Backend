from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'dev.db')}"
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProdConfig(Config):
    # Get the DATABASE_URL environment variable, used by Heroku/Render in production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Ensure DATABASE_URL is set, otherwise raise an error
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("Missing required DATABASE_URL environment variable.")
    
    DEBUG = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_ECHO = False
    TESTING = True
