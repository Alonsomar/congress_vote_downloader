import requests
import json
import time
from xml.etree import ElementTree as ET
import pymongo

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "votaciones_chile"

# Conexión a MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    diputados_collection = db["diputados_periodo_legislativo"]
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    exit()

def fetch_diputados_periodo():
    url_base = "https://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Periodo"
    periodo_id = 1
    consecutive_empty_responses = 0
    all_diputados = []

    while consecutive_empty_responses < 4:
        params = {"prmPeriodoID": periodo_id}
        response = requests.get(url_base, params=params)
        
        if response.status_code == 200:
            content = response.content.decode("utf-8")
            if "<Diputado>" in content:
                diputados = parse_diputados(content)
                all_diputados.extend(diputados)
                almacenar_diputados(diputados)
                print(f"Período {periodo_id}: {len(diputados)} diputados encontrados y almacenados.")
                consecutive_empty_responses = 0
            else:
                print(f"Período {periodo_id}: sin datos.")
                consecutive_empty_responses += 1
        else:
            print(f"Error en el request del período {periodo_id}: {response.status_code}")
            break
        
        periodo_id += 1
        time.sleep(0.3)  # Pausa para no sobrecargar el servidor

    print(f"Proceso completado. {len(all_diputados)} diputados procesados.")

def parse_diputados(content):
    """Extraer datos de diputados desde la respuesta XML."""
    diputados = []
    root = ET.fromstring(content)
    namespace = {"ns": "http://tempuri.org/"}

    for diputado in root.findall("ns:Diputado", namespace):
        diputado_data = {
            "DIPID": diputado.find("ns:DIPID", namespace).text if diputado.find("ns:DIPID", namespace) is not None else None,
            "Nombre": diputado.find("ns:Nombre", namespace).text if diputado.find("ns:Nombre", namespace) is not None else None,
            "Nombre2": diputado.find("ns:Nombre2", namespace).text if diputado.find("ns:Nombre2", namespace) is not None else None,
            "Apellido_Paterno": diputado.find("ns:Apellido_Paterno", namespace).text if diputado.find("ns:Apellido_Paterno", namespace) is not None else None,
            "Apellido_Materno": diputado.find("ns:Apellido_Materno", namespace).text if diputado.find("ns:Apellido_Materno", namespace) is not None else None,
            "Fecha_Nacimiento": diputado.find("ns:Fecha_Nacimiento", namespace).text if diputado.find("ns:Fecha_Nacimiento", namespace) is not None else None,
            "Sexo": diputado.find("ns:Sexo", namespace).text if diputado.find("ns:Sexo", namespace) is not None else None,
        }
        diputados.append(diputado_data)
    return diputados

def almacenar_diputados(diputados):
    """Almacena los datos de diputados en MongoDB."""
    if diputados:
        for diputado in diputados:
            diputados_collection.update_one(
                {"DIPID": diputado["DIPID"]},
                {"$set": diputado},
                upsert=True
            )
        print(f"Se almacenaron {len(diputados)} registros de diputados.")
    else:
        print("No hay registros de diputados para almacenar.")

if __name__ == "__main__":
    fetch_diputados_periodo()
