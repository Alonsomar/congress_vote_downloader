# clean_diputados.py
from utils.logger import get_logger
from .utils_clean import normalize_date, normalize_name, normalize_gender
from pymongo import UpdateOne

logger = get_logger(__name__)

def clean_diputados(db):
    """
    Limpia y normaliza los datos de diputados desde raw_diputados a diputados_final.
    
    Args:
        db: Conexión a la base de datos MongoDB
    """
    raw_diputados = db["raw_diputados_periodo_legislativo"]
    dip_final = db["diputados_final"]
    
    # Crear índice para DIPID si no existe
    dip_final.create_index("DIPID", unique=True)
    
    # Preparar operaciones bulk
    bulk_operations = []
    processed = 0
    errors = 0
    
    for d in raw_diputados.find():
        try:
            # Normalizar campos
            nombre = normalize_name(d.get('Nombre', ''))
            apellido_paterno = normalize_name(d.get('Apellido_Paterno', ''))
            apellido_materno = normalize_name(d.get('Apellido_Materno', ''))
            nombre_completo = f"{nombre} {apellido_paterno} {apellido_materno}".strip()
            
            # Crear documento limpio
            doc = {
                "DIPID": d.get("DIPID"),
                "nombre": nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "nombre_completo": nombre_completo,
                "fecha_nacimiento": normalize_date(d.get("Fecha_Nacimiento")),
                "sexo": normalize_gender(d.get("Sexo")),
                "raw_data": d  # Mantener datos originales por referencia
            }
            
            # Validar campos requeridos
            if not doc["DIPID"]:
                logger.warning(f"Diputado sin DIPID: {nombre_completo}")
                errors += 1
                continue
                
            # Crear operación de actualización
            bulk_operations.append(
                UpdateOne(
                    {"DIPID": doc["DIPID"]},
                    {"$set": doc},
                    upsert=True
                )
            )
            
            processed += 1
            
            # Ejecutar en lotes de 1000
            if len(bulk_operations) >= 1000:
                dip_final.bulk_write(bulk_operations)
                bulk_operations = []
                logger.info(f"Procesados {processed} diputados...")
                
        except Exception as e:
            logger.error(f"Error procesando diputado {d.get('DIPID')}: {str(e)}")
            errors += 1
            
    # Ejecutar operaciones restantes
    if bulk_operations:
        dip_final.bulk_write(bulk_operations)
    
    # Logging final
    logger.info(f"Proceso completado: {processed} diputados procesados, {errors} errores")
    logger.info(f"Total de diputados en colección final: {dip_final.count_documents({})}")
