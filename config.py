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
    # Get environment variables with fallback to raise an error if missing
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
    db_port = os.getenv('DB_PORT', '5432')  # Default to '5432' if not set
    db_name = os.getenv('DB_NAME')

    # Validate that required environment variables are provided
    if not db_user or not db_password or not db_name:
        raise ValueError("Missing required database credentials (DB_USER, DB_PASSWORD, DB_NAME).")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    DEBUG = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_ECHO = False
    TESTING = True
