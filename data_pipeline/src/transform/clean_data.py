from utils.db_connection import get_mongodb_connection 
from utils.logger import get_logger
from .clean_diputados import clean_diputados
from .clean_proyectos import clean_proyectos
# from clean_votaciones import clean_votaciones
# from clean_asistencia import clean_asistencia

logger = get_logger(__name__)

def main():
    client, db = get_mongodb_connection()
    
    logger.info("Iniciando limpieza de datos")
    
    # 1. Limpiar diputados
    logger.info("Limpiando diputados...")
    clean_diputados(db)
    
    # 2. Limpiar proyectos
    logger.info("Limpiando proyectos...")
    clean_proyectos(db)
    
    # # 3. Limpiar votaciones (ya tengo diputados y proyectos limpios)
    # logger.info("Limpiando votaciones...")
    # clean_votaciones(db)
    
    # # 4. Limpiar asistencia (ya tengo diputados limpios)
    # logger.info("Limpiando asistencia...")
    # clean_asistencia(db)
    
    logger.info("Limpieza completa")



if __name__ == "__main__":
    main()