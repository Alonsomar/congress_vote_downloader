import requests
import xml.etree.ElementTree as ET
from utils.db_connection import get_mongodb_connection
from utils.logger import get_logger

logger = get_logger(__name__)

# URL base
DETALLE_VOTACION_URL = "https://opendata.camara.cl/wscamaradiputados.asmx/getVotacion_Detalle"



# Función para obtener el detalle de una votación
def get_votacion_detalle(votacion_id):
    """
    Recupera el detalle de una votación de diputados.
    """
    try:
        response = requests.get(f"{DETALLE_VOTACION_URL}?prmVotacionID={votacion_id}")
        response.raise_for_status()
        detalle_votacion = {}
        root = ET.fromstring(response.content)
        
        # Extraer datos principales
        detalle_votacion["ID"] = root.find("{http://tempuri.org/}ID").text
        detalle_votacion["Fecha"] = root.find("{http://tempuri.org/}Fecha").text
        detalle_votacion["Tipo"] = root.find("{http://tempuri.org/}Tipo").text
        detalle_votacion["Resultado"] = root.find("{http://tempuri.org/}Resultado").text
        detalle_votacion["Quorum"] = root.find("{http://tempuri.org/}Quorum").text
        
        detalle_votacion["Sesion"] = {
            "ID": root.find(".//{http://tempuri.org/}Sesion/{http://tempuri.org/}ID").text,
            "Numero": root.find(".//{http://tempuri.org/}Sesion/{http://tempuri.org/}Numero").text,
            "Fecha": root.find(".//{http://tempuri.org/}Sesion/{http://tempuri.org/}Fecha").text
        }
        detalle_votacion["Boletin"] = root.find("{http://tempuri.org/}Boletin").text
        
        # Extraer información de votos
        detalle_votacion["Votos"] = []
        for voto in root.findall(".//{http://tempuri.org/}Voto"):
            detalle_votacion["Votos"].append({
                "DIPID": voto.find(".//{http://tempuri.org/}DIPID").text,
                "Nombre": voto.find(".//{http://tempuri.org/}Nombre").text,
                "Apellido_Paterno": voto.find(".//{http://tempuri.org/}Apellido_Paterno").text,
                "Apellido_Materno": voto.find(".//{http://tempuri.org/}Apellido_Materno").text,
                "Opcion": voto.find(".//{http://tempuri.org/}Opcion").text
            })
        
        # Extraer información de pareos
        detalle_votacion["Pareos"] = []
        for pareo in root.findall(".//{http://tempuri.org/}Pareo"):
            detalle_votacion["Pareos"].append({
                "Diputado1": {
                    "DIPID": pareo.find(".//{http://tempuri.org/}Diputado1/{http://tempuri.org/}DIPID").text,
                    "Nombre": pareo.find(".//{http://tempuri.org/}Diputado1/{http://tempuri.org/}Nombre").text,
                    "Apellido_Paterno": pareo.find(".//{http://tempuri.org/}Diputado1/{http://tempuri.org/}Apellido_Paterno").text,
                    "Apellido_Materno": pareo.find(".//{http://tempuri.org/}Diputado1/{http://tempuri.org/}Apellido_Materno").text
                },
                "Diputado2": {
                    "DIPID": pareo.find(".//{http://tempuri.org/}Diputado2/{http://tempuri.org/}DIPID").text,
                    "Nombre": pareo.find(".//{http://tempuri.org/}Diputado2/{http://tempuri.org/}Nombre").text,
                    "Apellido_Paterno": pareo.find(".//{http://tempuri.org/}Diputado2/{http://tempuri.org/}Apellido_Paterno").text,
                    "Apellido_Materno": pareo.find(".//{http://tempuri.org/}Diputado2/{http://tempuri.org/}Apellido_Materno").text
                }
            })
        
        return detalle_votacion
    except Exception as e:
        logger.error(f"Error al obtener detalle de votación {votacion_id}: {e}")
        return None

# Almacenamiento en MongoDB
def almacenar_detalle_votacion(detalle_votacion, votacion_detalle_collection):
    """
    Almacena el detalle de una votación en MongoDB.
    """
    if detalle_votacion:
        votacion_id = detalle_votacion["ID"]
        votacion_detalle_collection.update_one(
            {"ID": votacion_id},
            {"$set": detalle_votacion},
            upsert=True
        )
        logger.info(f"Detalle de votación {votacion_id} almacenado correctamente.")

def main():
    logger.info("Iniciando la descarga de detalle de votaciones.")

    # Conexión a MongoDB
    client, db = get_mongodb_connection()
    votaciones_diputados_collection = db["raw_votaciones_diputados"]
    votacion_detalle_collection = db["raw_votacion_detalle"]

    # Obtener IDs de votaciones de la colección `votaciones_diputados`
    votaciones_cursor = votaciones_diputados_collection.find({}, {"ID": 1})
    for documento in votaciones_cursor:
        votacion_id = documento["ID"]
        logger.info(f"Procesando votación {votacion_id}...")
        
        # Obtener detalle de votación
        detalle_votacion = get_votacion_detalle(votacion_id)
        
        # Almacenar en MongoDB
        almacenar_detalle_votacion(detalle_votacion, votacion_detalle_collection)


# Proceso principal
if __name__ == "__main__":
    main()
