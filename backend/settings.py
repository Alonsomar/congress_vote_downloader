import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'infrastructure', 'env', 'dev.env'))

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://root:example@mongo:27017/')

# Ajustar otras configuraciones...
