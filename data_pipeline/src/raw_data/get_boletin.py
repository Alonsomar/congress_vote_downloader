import requests
from utils.db_connection import get_mongodb_connection
from utils.logger import get_logger
logger = get_logger(__name__)

# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_BOLETIN = "/wscamaradiputados.asmx/getSesionBoletinXML"


def obtener_boletin(sesion_id):
    """Obtiene el boletín de una sesión por su ID."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_BOLETIN}?prmSesionID={sesion_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Estado de la respuesta para boletín de sesión {sesion_id}: {response.status_code}")
        return response.text  # Guardar como texto para preservar el formato
    except Exception as e:
        logger.error(f"Error al obtener boletín para sesión {sesion_id}: {e}")
        return None


def almacenar_boletin(sesion_id, boletin_data, boletin_collection):
    """Almacena el boletín en MongoDB."""
    if boletin_data:
        boletin_collection.update_one(
            {"SesionID": sesion_id},
            {"$set": {"BoletinXML": boletin_data}},
            upsert=True,
        )
        logger.info(f"Boletín de la sesión {sesion_id} almacenado.")
    else:
        logger.info(f"No se almacenó boletín para la sesión {sesion_id}.")

def main():
    logger.info("Iniciando la descarga de boletines.")

    # Conexión a MongoDB
    client, db = get_mongodb_connection()
    sesiones_collection = db["raw_sesiones_diputados"]
    boletin_collection = db["raw_boletines_sesiones"]
 
    # Obtener sesiones desde MongoDB
    sesiones = sesiones_collection.find()

    for sesion in sesiones:
        sesion_id = sesion["ID"]
        logger.info(f"Procesando boletín para sesión ID: {sesion_id}")
        boletin = obtener_boletin(sesion_id)
        almacenar_boletin(sesion_id, boletin, boletin_collection)


if __name__ == "__main__":
    main()
