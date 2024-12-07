import requests
import pymongo
import xml.etree.ElementTree as ET

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "votaciones_chile"

# Conexión a MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    sesiones_collection = db["sesiones_diputados"]
    asistencia_collection = db["asistencia_sesiones"]
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_ASISTENCIA = "/wscamaradiputados.asmx/getSesionDetalle"


def obtener_asistencia(sesion_id):
    """Obtiene la asistencia de una sesión por su ID."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_ASISTENCIA}?prmSesionID={sesion_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Estado de la respuesta para sesión {sesion_id}: {response.status_code}")
        return parsear_asistencia(response.content, sesion_id)
    except Exception as e:
        print(f"Error al obtener asistencia para sesión {sesion_id}: {e}")
        return []


def parsear_asistencia(xml_data, sesion_id):
    """Parsea la asistencia desde la respuesta XML."""
    namespaces = {"ns": "http://tempuri.org/"}  # Registra el namespace
    root = ET.fromstring(xml_data)
    asistentes = []
    for asistente in root.findall(".//ns:AsistenteSala", namespaces=namespaces):
        try:
            data = {
                "SesionID": sesion_id,
                "DiputadoID": int(asistente.find("ns:Diputado/ns:DIPID", namespaces).text),
                "Nombre": asistente.find("ns:Diputado/ns:Nombre", namespaces).text,
                "ApellidoPaterno": asistente.find("ns:Diputado/ns:Apellido_Paterno", namespaces).text,
                "ApellidoMaterno": asistente.find("ns:Diputado/ns:Apellido_Materno", namespaces).text,
                "AsistenciaCodigo": int(asistente.find("ns:Asistencia", namespaces).attrib.get("Codigo")),
                "Asiste": asistente.find("ns:Asistencia", namespaces).attrib.get("Asiste"),
                "EstadoAsistencia": asistente.find("ns:Asistencia", namespaces).text,
            }
            asistentes.append(data)
        except AttributeError as e:
            print(f"Error al procesar un asistente: {e}")
    return asistentes


def almacenar_asistencia(asistentes):
    """Almacena la asistencia en MongoDB."""
    if asistentes:
        for asistente in asistentes:
            asistencia_collection.update_one(
                {"SesionID": int(asistente["SesionID"]), "DiputadoID": int(asistente["DiputadoID"])},
                {"$set": asistente},
                upsert=True,
            )
        print(f"Se almacenaron {len(asistentes)} registros de asistencia.")
    else:
        print("No hay registros de asistencia para almacenar.")


if __name__ == "__main__":
    # Obtener sesiones desde MongoDB
    sesiones = sesiones_collection.find()

    for sesion in sesiones:
        sesion_id = sesion["ID"]
        print(f"Procesando asistencia para sesión ID: {sesion_id}")
        asistencia = obtener_asistencia(sesion_id)
        almacenar_asistencia(asistencia)
