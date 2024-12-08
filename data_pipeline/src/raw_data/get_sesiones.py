import requests
import xml.etree.ElementTree as ET
from utils.db_connection import get_mongodb_connection
from utils.logger import get_logger
logger = get_logger(__name__)

# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_SESIONES = "/wscamaradiputados.asmx/getSesiones"


def obtener_sesiones(legislatura_id):
    """Obtiene las sesiones asociadas a una legislatura desde el endpoint."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_SESIONES}?prmLegislaturaID={legislatura_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Estado de la respuesta para legislatura {legislatura_id}: {response.status_code}")
        return parsear_sesiones(response.content, legislatura_id)
    except Exception as e:
        logger.error(f"Error al obtener sesiones para legislatura {legislatura_id}: {e}")
        return []


def parsear_sesiones(xml_data, legislatura_id):
    """Parsea las sesiones desde la respuesta XML."""
    namespaces = {"ns": "http://tempuri.org/"}  # Registra el namespace
    root = ET.fromstring(xml_data)
    sesiones = []
    for sesion in root.findall(".//ns:Sesion", namespaces=namespaces):
        try:
            data = {
                "ID": int(sesion.find("ns:ID", namespaces).text),
                "Numero": int(sesion.find("ns:Numero", namespaces).text),
                "Fecha": sesion.find("ns:Fecha", namespaces).text,
                "FechaTermino": sesion.find("ns:FechaTermino", namespaces).text,
                "Tipo": sesion.find("ns:Tipo", namespaces).text,
                "TipoCodigo": int(sesion.find("ns:Tipo", namespaces).attrib.get("Codigo")),
                "Estado": sesion.find("ns:Estado", namespaces).text,
                "EstadoCodigo": int(sesion.find("ns:Estado", namespaces).attrib.get("Codigo")),
                "LegislaturaID": legislatura_id,
            }
            sesiones.append(data)
        except AttributeError as e:
            logger.error(f"Error al procesar una sesión: {e}")
    return sesiones


def almacenar_sesiones(sesiones, sesiones_collection):
    """Almacena las sesiones en MongoDB."""
    if sesiones:
        for sesion in sesiones:
            sesiones_collection.update_one(
                {"ID": sesion["ID"]}, {"$set": sesion}, upsert=True
            )
        logger.info(f"Se almacenaron {len(sesiones)} sesiones.")
    else:
        logger.info("No hay sesiones para almacenar.")

def main():
    logger.info("Iniciando extracción de sesiones")

    # Conexión a MongoDB
    client, db = get_mongodb_connection()
    legislaturas_collection = db["raw_legislaturas_diputados"]
    sesiones_collection = db["raw_sesiones_diputados"]

    # Obtener legislaturas desde MongoDB
    legislaturas = legislaturas_collection.find({"ID": {"$gte": 42}})

    for legislatura in legislaturas:
        legislatura_id = legislatura["ID"]
        logger.info(f"Procesando legislatura ID: {legislatura_id}")
        sesiones = obtener_sesiones(legislatura_id)
        almacenar_sesiones(sesiones, sesiones_collection)


if __name__ == "__main__":
    main()
