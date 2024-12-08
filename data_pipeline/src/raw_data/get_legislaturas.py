import requests
import xml.etree.ElementTree as ET
from utils.db_connection import get_mongodb_connection
from utils.logger import get_logger
logger = get_logger(__name__)


# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_LEGISLATURAS = "/wscamaradiputados.asmx/getLegislaturas"


def obtener_legislaturas():
    """Obtiene las legislaturas desde el endpoint."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_LEGISLATURAS}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa
        logger.info(f"Estado de la respuesta: {response.status_code}")
        logger.info(f"Contenido de la respuesta: {response.text[:500]}...")  # Solo imprime una parte para depuración
        legislaturas = parsear_legislaturas(response.content)
        logger.info(f"Legislaturas obtenidas: {len(legislaturas)}")
        return legislaturas
    except Exception as e:
        logger.error(f"Error al obtener legislaturas: {e}")
        return []


def parsear_legislaturas(xml_data):
    """Parsea las legislaturas desde la respuesta XML."""
    namespaces = {"ns": "http://tempuri.org/"}  # Registra el namespace
    root = ET.fromstring(xml_data)
    legislaturas = []
    for legislatura in root.findall(".//ns:Legislatura", namespaces=namespaces):
        try:
            data = {
                "ID": int(legislatura.find("ns:ID", namespaces).text),
                "Numero": int(legislatura.find("ns:Numero", namespaces).text),
                "Tipo": legislatura.find("ns:Tipo", namespaces).text,
                "TipoCodigo": legislatura.find("ns:Tipo", namespaces).attrib.get("Codigo"),
                "FechaInicio": legislatura.find("ns:FechaInicio", namespaces).text,
                "FechaTermino": legislatura.find("ns:FechaTermino", namespaces).text,
            }
            legislaturas.append(data)
        except AttributeError as e:
            logger.error(f"Error al procesar una legislatura: {e}")
    return legislaturas


def almacenar_legislaturas(legislaturas, legislaturas_collection):
    """Almacena las legislaturas en MongoDB."""
    if legislaturas:
        for legislatura in legislaturas:
            legislaturas_collection.update_one(
                {"ID": legislatura["ID"]}, {"$set": legislatura}, upsert=True
            )
        logger.info(f"Se almacenaron {len(legislaturas)} legislaturas.")
    else:
        logger.info("No hay legislaturas para almacenar.")

def main():
    logger.info("Iniciando la descarga de legislaturas.")

    # Conexión a MongoDB
    client, db = get_mongodb_connection()
    legislaturas_collection = db["raw_legislaturas_diputados"]

    # Obtener y almacenar legislaturas
    legislaturas = obtener_legislaturas()
    almacenar_legislaturas(legislaturas, legislaturas_collection)


if __name__ == "__main__":
    main()
