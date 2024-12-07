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
    legislaturas_collection = db["legislaturas_diputados"]
    sesiones_collection = db["sesiones_diputados"]
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_SESIONES = "/wscamaradiputados.asmx/getSesiones"


def obtener_sesiones(legislatura_id):
    """Obtiene las sesiones asociadas a una legislatura desde el endpoint."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_SESIONES}?prmLegislaturaID={legislatura_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Estado de la respuesta para legislatura {legislatura_id}: {response.status_code}")
        return parsear_sesiones(response.content, legislatura_id)
    except Exception as e:
        print(f"Error al obtener sesiones para legislatura {legislatura_id}: {e}")
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
            print(f"Error al procesar una sesión: {e}")
    return sesiones


def almacenar_sesiones(sesiones):
    """Almacena las sesiones en MongoDB."""
    if sesiones:
        for sesion in sesiones:
            sesiones_collection.update_one(
                {"ID": sesion["ID"]}, {"$set": sesion}, upsert=True
            )
        print(f"Se almacenaron {len(sesiones)} sesiones.")
    else:
        print("No hay sesiones para almacenar.")


if __name__ == "__main__":
    # Obtener legislaturas desde MongoDB
    legislaturas = legislaturas_collection.find({"ID": {"$gte": 42}})

    for legislatura in legislaturas:
        legislatura_id = legislatura["ID"]
        print(f"Procesando legislatura ID: {legislatura_id}")
        sesiones = obtener_sesiones(legislatura_id)
        almacenar_sesiones(sesiones)
