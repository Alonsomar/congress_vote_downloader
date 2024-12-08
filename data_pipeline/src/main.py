import raw_data
from transform.clean_data import main as clean_data_main
from utils.logger import get_logger

logger = get_logger(__name__)

# Ejecutar extracción
scripts_order = [
    ("get_legislaturas", raw_data.get_legislaturas),
    ("get_periodos", raw_data.get_periodos),
    ("get_diputados_periodo", raw_data.get_diputados_periodo),
    ("get_sesiones", raw_data.get_sesiones),
    ("get_boletin", raw_data.get_boletin),
    ("get_asistencia", raw_data.get_asistencia),
    ("get_proyectos", raw_data.get_proyectos),
    ("get_votaciones", raw_data.get_votaciones),
    ("get_votacion_detalle", raw_data.get_votacion_detalle),
]

for script_name, script_main in scripts_order:
    logger.info(f"Ejecutando {script_name}")
    try:
        script_main()  # Ejecuta la función principal de cada módulo
        logger.info(f"Finalizado {script_name}")
    except Exception as e:
        logger.error(f"Error ejecutando {script_name}: {e}")

# Ejecutar limpieza
logger.info("Iniciando limpieza y normalización")
try:
    clean_data_main()
    logger.info("Limpieza completada")
except Exception as e:
    logger.error(f"Error durante la limpieza: {e}")
