import requests
import pymongo

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "votaciones_chile"

# Conexión a MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    sesiones_collection = db["sesiones_diputados"]
    boletin_collection = db["boletines_sesiones"]
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_BOLETIN = "/wscamaradiputados.asmx/getSesionBoletinXML"


def obtener_boletin(sesion_id):
    """Obtiene el boletín de una sesión por su ID."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_BOLETIN}?prmSesionID={sesion_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Estado de la respuesta para boletín de sesión {sesion_id}: {response.status_code}")
        return response.text  # Guardar como texto para preservar el formato
    except Exception as e:
        print(f"Error al obtener boletín para sesión {sesion_id}: {e}")
        return None


def almacenar_boletin(sesion_id, boletin_data):
    """Almacena el boletín en MongoDB."""
    if boletin_data:
        boletin_collection.update_one(
            {"SesionID": sesion_id},
            {"$set": {"BoletinXML": boletin_data}},
            upsert=True,
        )
        print(f"Boletín de la sesión {sesion_id} almacenado.")
    else:
        print(f"No se almacenó boletín para la sesión {sesion_id}.")


if __name__ == "__main__":
    # Obtener sesiones desde MongoDB
    sesiones = sesiones_collection.find()

    for sesion in sesiones:
        sesion_id = sesion["ID"]
        print(f"Procesando boletín para sesión ID: {sesion_id}")
        boletin = obtener_boletin(sesion_id)
        almacenar_boletin(sesion_id, boletin)
