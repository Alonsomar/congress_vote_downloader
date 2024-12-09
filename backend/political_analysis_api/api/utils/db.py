import os
from pymongo import MongoClient
from dotenv import load_dotenv
from .logger import get_logger

logger = get_logger(__name__)

def load_environment():
    """Load environment variables from the appropriate .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'infrastructure', 'env', 'dev.env')
    load_dotenv(env_path)


def get_mongodb_connection():
    """Get MongoDB connection with configuration from environment variables"""
    load_environment()
    
    # Get MongoDB URI from environment variable or use default
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    database_name = os.getenv('DB_NAME', 'votaciones_chile')
    
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        logger.info("Conexión exitosa a MongoDB")
        return client, db
    except Exception as e:
        logger.error(f"Error al conectar con MongoDB: {e}")
        raise

# Initialize database connection
client, db = get_mongodb_connection()



