import requests
from utils.db_connection import get_mongodb_connection
from utils.logger import get_logger
logger = get_logger(__name__)

# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_PERIODOS = "/ws/periodosLegislativos.asmx/getPeriodosLegislativos"


def obtener_periodos_legislativos():
    """Obtiene los períodos legislativos desde el endpoint."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_PERIODOS}"
    try:
        logger.info(f"Obteniendo períodos legislativos desde {url}")
        response = requests.get(url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa
        periodos = response.json()  # Cambiar según formato, si es XML, parsear adecuadamente
        logger.info(f"Periodos legislativos obtenidos: {len(periodos)}")
        return periodos
    except Exception as e:
        logger.error(f"Error al obtener períodos legislativos: {e}")
        return []


def almacenar_periodos(periodos, periodos_collection):
    """Almacena los períodos legislativos en MongoDB."""
    if periodos:
        for periodo in periodos:
            periodos_collection.update_one(
                {"Id": periodo["Id"]}, {"$set": periodo}, upsert=True
            )
        logger.info(f"Se almacenaron {len(periodos)} períodos legislativos.")
    else:
        logger.info("No hay períodos legislativos para almacenar.")

def main():
    logger.info("Iniciando la descarga de períodos legislativos.")

    # Conexión a MongoDB
    client, db = get_mongodb_connection()
    periodos_collection = db["raw_periodos_legislativos"]
        
    periodos = obtener_periodos_legislativos()
    almacenar_periodos(periodos, periodos_collection)

if __name__ == "__main__":
    main()
