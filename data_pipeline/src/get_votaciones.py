import requests
import pymongo
import xml.etree.ElementTree as ET

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "votaciones_chile"

# URLs base
DIPUTADOS_URL = "https://opendata.camara.cl/wscamaradiputados.asmx/getVotaciones_Boletin"
SENADORES_URL = "https://tramitacion.senado.cl/wspublico/votaciones.php"

# Conexión a MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    diputados_collection = db["votaciones_diputados"]
    senadores_collection = db["votaciones_senadores"]
    proyectos_collection = db["proyectos"]  # Colección donde están los boletines
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

# Función para obtener votaciones de diputados
def get_votaciones_diputados(boletin):
    """
    Recupera las votaciones desde la Cámara de Diputados.
    """
    try:
        response = requests.get(f"{DIPUTADOS_URL}?prmBoletin={boletin}")
        response.raise_for_status()
        votaciones = []
        root = ET.fromstring(response.content)
        for votacion in root.findall(".//{http://tempuri.org/}Votacion"):
            data = {
                "ID": votacion.find("{http://tempuri.org/}ID").text,
                "Fecha": votacion.find("{http://tempuri.org/}Fecha").text,
                "Tipo": votacion.find("{http://tempuri.org/}Tipo").text,
                "Resultado": votacion.find("{http://tempuri.org/}Resultado").text,
                "Quorum": votacion.find("{http://tempuri.org/}Quorum").text,
                "Sesion": {
                    "ID": votacion.find(".//{http://tempuri.org/}ID").text,
                    "Numero": votacion.find(".//{http://tempuri.org/}Numero").text,
                    "Fecha": votacion.find(".//{http://tempuri.org/}Fecha").text,
                },
                "Boletin": votacion.find("{http://tempuri.org/}Boletin").text,
                "TotalAfirmativos": votacion.find("{http://tempuri.org/}TotalAfirmativos").text,
                "TotalNegativos": votacion.find("{http://tempuri.org/}TotalNegativos").text,
                "TotalAbstenciones": votacion.find("{http://tempuri.org/}TotalAbstenciones").text,
            }
            votaciones.append(data)
        return votaciones
    except Exception as e:
        print(f"Error al obtener votaciones de diputados para boletín {boletin}: {e}")
        return []

# Función para obtener votaciones de senadores
def get_votaciones_senadores(boletin):
    """
    Recupera las votaciones desde el Senado.
    """
    try:
        response = requests.get(f"{SENADORES_URL}?boletin={boletin}")
        response.raise_for_status()
        votaciones = []
        root = ET.fromstring(response.content)
        for votacion in root.findall(".//votacion"):
            data = {
                "Sesion": votacion.find("SESION").text,
                "Fecha": votacion.find("FECHA").text,
                "Tema": votacion.find("TEMA").text,
                "Quorum": votacion.find("QUORUM").text,
                "TipoVotacion": votacion.find("TIPOVOTACION").text,
                "Etapa": votacion.find("ETAPA").text,
                "Si": votacion.find("SI").text,
                "No": votacion.find("NO").text,
                "Abstencion": votacion.find("ABSTENCION").text,
                "DetalleVotacion": [
                    {
                        "Parlamentario": voto.find("PARLAMENTARIO").text,
                        "Seleccion": voto.find("SELECCION").text,
                    }
                    for voto in votacion.findall(".//VOTO")
                ],
            }
            votaciones.append(data)
        return votaciones
    except Exception as e:
        print(f"Error al obtener votaciones de senadores para boletín {boletin}: {e}")
        return []

# Almacenamiento en MongoDB
def almacenar_votaciones(collection, votaciones, boletin):
    """
    Almacena las votaciones en la colección correspondiente.
    """
    for votacion in votaciones:
        votacion["Boletin"] = boletin
        collection.update_one(
            {"Boletin": boletin, "ID": votacion.get("ID")},
            {"$set": votacion},
            upsert=True
        )
    print(f"{len(votaciones)} votaciones almacenadas para boletín {boletin}")

# Proceso principal
if __name__ == "__main__":
    # Obtener boletines de la colección `proyectos`
    boletines_cursor = proyectos_collection.find({"Boletin": {"$exists": True}})
    for documento in boletines_cursor:
        boletin = documento["Boletin"]
        boletin_base = boletin.split("-")[0]  # Usar los primeros 4 dígitos
        print(f"Procesando boletín {boletin_base}")

        # Obtener y almacenar votaciones de diputados
        votaciones_diputados = get_votaciones_diputados(boletin_base)
        almacenar_votaciones(diputados_collection, votaciones_diputados, boletin_base)

        # Obtener y almacenar votaciones de senadores
        votaciones_senadores = get_votaciones_senadores(boletin_base)
        almacenar_votaciones(senadores_collection, votaciones_senadores, boletin_base)
