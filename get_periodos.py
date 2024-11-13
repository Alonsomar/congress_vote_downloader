import requests
import pymongo

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "votaciones_chile"

# Conexión a MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    periodos_collection = db["periodos_legislativos"]
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# Configuración del endpoint
BASE_URL_CAMARA = "https://opendata.camara.cl"
ENDPOINT_PERIODOS = "/ws/periodosLegislativos.asmx/getPeriodosLegislativos"


def obtener_periodos_legislativos():
    """Obtiene los períodos legislativos desde el endpoint."""
    url = f"{BASE_URL_CAMARA}{ENDPOINT_PERIODOS}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa
        periodos = response.json()  # Cambiar según formato, si es XML, parsear adecuadamente
        print(f"Periodos legislativos obtenidos: {len(periodos)}")
        return periodos
    except Exception as e:
        print(f"Error al obtener períodos legislativos: {e}")
        return []


def almacenar_periodos(periodos):
    """Almacena los períodos legislativos en MongoDB."""
    if periodos:
        for periodo in periodos:
            periodos_collection.update_one(
                {"Id": periodo["Id"]}, {"$set": periodo}, upsert=True
            )
        print(f"Se almacenaron {len(periodos)} períodos legislativos.")
    else:
        print("No hay períodos legislativos para almacenar.")


if __name__ == "__main__":
    # Obtener y almacenar los períodos legislativos
    periodos = obtener_periodos_legislativos()
    almacenar_periodos(periodos)
