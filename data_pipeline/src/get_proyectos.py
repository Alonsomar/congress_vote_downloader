import requests
import pymongo
import xml.etree.ElementTree as ET
import re

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "votaciones_chile"

# Conexión a MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    boletines_collection = db["boletines_sesiones"]
    proyectos_collection = db["proyectos"]
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# Configuración del endpoint
BASE_URL_TRAMITACION = "https://tramitacion.senado.cl/wspublico/tramitacion.php"

def extraer_boletines(boletin_xml):
    """
    Extrae los números de boletín del XML almacenado en la colección boletines_sesiones.
    """
    boletines = set()
    try:
        root = ET.fromstring(boletin_xml)
        for element in root.iter():
            if element.text and re.search(r'\b\d{4}-\d{2}\b', element.text):
                matches = re.findall(r'\b\d{4}-\d{2}\b', element.text)
                boletines.update(matches)
    except ET.ParseError as e:
        print(f"Error al parsear XML: {e}")
    return list(boletines)

def descargar_proyecto(boletin):
    """
    Descarga los datos del proyecto legislativo desde el endpoint del Senado.
    """
    boletin_base = boletin.split("-")[0]  # Solo tomar los primeros 4 dígitos
    url = f"{BASE_URL_TRAMITACION}?boletin={boletin_base}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Datos descargados para boletín {boletin}")
        return response.text
    except Exception as e:
        print(f"Error al descargar datos para boletín {boletin}: {e}")
        return None

def almacenar_proyecto(boletin, data):
    """
    Almacena el proyecto descargado en MongoDB.
    """
    if data:
        proyectos_collection.update_one(
            {"Boletin": boletin},
            {"$set": {"Boletin": boletin, "Datos": data}},
            upsert=True,
        )
        print(f"Datos almacenados para boletín {boletin}")
    else:
        print(f"No se almacenaron datos para boletín {boletin}")

if __name__ == "__main__":
    # Obtener boletines no procesados desde la colección boletines_sesiones
    boletines_cursor = boletines_collection.find({"BoletinXML": {"$exists": True}})
    for documento in boletines_cursor:
        boletin_xml = documento.get("BoletinXML", "")
        boletines = extraer_boletines(boletin_xml)
        
        for boletin in boletines:
            # Comprobar si el boletín ya está almacenado
            existe = proyectos_collection.find_one({"Boletin": boletin})
            if existe:
                print(f"El boletín {boletin} ya está almacenado. Saltando...")
                continue
            
            print(f"Procesando boletín {boletin}")
            proyecto_data = descargar_proyecto(boletin)
            almacenar_proyecto(boletin, proyecto_data)
