import requests
import xml.etree.ElementTree as ET
import re
from utils.db_connection import get_mongodb_connection
from utils.logger import get_logger

logger = get_logger(__name__)


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
        logger.error(f"Error al parsear XML: {e}")
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
        logger.info(f"Datos descargados para boletín {boletin}")
        return response.text
    except Exception as e:
        logger.error(f"Error al descargar datos para boletín {boletin}: {e}")
        return None

def almacenar_proyecto(boletin, data, proyectos_collection):
    """
    Almacena el proyecto descargado en MongoDB.
    """
    if data:
        proyectos_collection.update_one(
            {"Boletin": boletin},
            {"$set": {"Boletin": boletin, "Datos": data}},
            upsert=True,
        )
        logger.info(f"Datos almacenados para boletín {boletin}")
    else:
        logger.info(f"No se almacenaron datos para boletín {boletin}")

def main():
    logger.info("Iniciando la descarga de proyectos.")

    # Conexión a MongoDB
    client, db = get_mongodb_connection()
    boletines_collection = db["raw_boletines_sesiones"]
    proyectos_collection = db["raw_proyectos"]

    # Obtener boletines no procesados desde la colección boletines_sesiones
    boletines_cursor = boletines_collection.find({"BoletinXML": {"$exists": True}})
    for documento in boletines_cursor:
        boletin_xml = documento.get("BoletinXML", "")
        boletines = extraer_boletines(boletin_xml)
        
        for boletin in boletines:
            # Comprobar si el boletín ya está almacenado
            existe = proyectos_collection.find_one({"Boletin": boletin})
            if existe:
                logger.info(f"El boletín {boletin} ya está almacenado. Saltando...")
                continue
            
            logger.info(f"Procesando boletín {boletin}")
            proyecto_data = descargar_proyecto(boletin)
            almacenar_proyecto(boletin, proyecto_data, proyectos_collection)
