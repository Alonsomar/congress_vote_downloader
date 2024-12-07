import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('../infrastructure/env/dev.env')  # Ajusta la ruta según tu estructura

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client["votaciones_chile"]

# Aquí la lógica de limpieza...
