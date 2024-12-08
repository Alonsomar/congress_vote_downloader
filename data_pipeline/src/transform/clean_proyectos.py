from utils.logger import get_logger
from .utils_clean import normalize_date
import xml.etree.ElementTree as ET
from pymongo import UpdateOne

logger = get_logger(__name__)

def parse_proyecto_xml(xml_data):
    """
    Parsea el XML de un proyecto y extrae la información relevante.
    
    Args:
        xml_data (str): String con el XML del proyecto
        
    Returns:
        dict: Diccionario con los datos normalizados del proyecto
    """
    try:
        root = ET.fromstring(xml_data)
        
        # Extraer datos básicos de descripción
        proyecto = {
            # Identificación
            "boletin": root.find(".//boletin").text if root.find(".//boletin") is not None else None,
            "titulo": root.find(".//titulo").text if root.find(".//titulo") is not None else None,
            
            # Estado actual
            "estado": root.find(".//estado").text if root.find(".//estado") is not None else None,
            "etapa": root.find(".//etapa").text if root.find(".//etapa") is not None else None,
            "subetapa": root.find(".//subetapa").text if root.find(".//subetapa") is not None else None,
            "urgencia_actual": root.find(".//urgencia_actual").text if root.find(".//urgencia_actual") is not None else None,
            
            # Datos de origen
            "fecha_ingreso": normalize_date(root.find(".//fecha_ingreso").text) if root.find(".//fecha_ingreso") is not None else None,
            "iniciativa": root.find(".//iniciativa").text if root.find(".//iniciativa") is not None else None,
            "camara_origen": root.find(".//camara_origen").text if root.find(".//camara_origen") is not None else None,
            "link_mensaje_mocion": root.find(".//link_mensaje_mocion").text if root.find(".//link_mensaje_mocion") is not None else None,
            
            # Datos de ley (si está publicada)
            "ley": {
                "numero": root.find(".//leynro").text if root.find(".//leynro") is not None else None,
                "fecha_publicacion": normalize_date(root.find(".//diariooficial").text) if root.find(".//diariooficial") is not None else None
            },
            
            # Proyectos refundidos
            "refundidos": [ref.text for ref in root.findall(".//refundidos/refundido") if ref.text]
        }
        
        # Extraer autores (parlamentarios)
        autores_section = root.find(".//autores")
        if autores_section is not None:
            autores = []
            for autor in autores_section.findall(".//PARLAMENTARIO"):
                if autor.text and autor.text.strip():
                    autores.append(autor.text.strip())
            if autores:
                proyecto["autores"] = autores
        
        # Extraer materias
        materias = root.findall(".//materia/DESCRIPCION")
        if materias:
            proyecto["materias"] = [materia.text.strip() for materia in materias if materia.text]
        
        # Extraer tramitación
        tramites = []
        for tramite in root.findall(".//tramite"):
            tramite_data = {
                "sesion": tramite.find("SESION").text if tramite.find("SESION") is not None else None,
                "fecha": normalize_date(tramite.find("FECHA").text) if tramite.find("FECHA") is not None else None,
                "descripcion": tramite.find("DESCRIPCIONTRAMITE").text if tramite.find("DESCRIPCIONTRAMITE") is not None else None,
                "etapa": tramite.find("ETAPDESCRIPCION").text if tramite.find("ETAPDESCRIPCION") is not None else None,
                "camara": tramite.find("CAMARATRAMITE").text if tramite.find("CAMARATRAMITE") is not None else None
            }
            tramites.append(tramite_data)
        if tramites:
            proyecto["tramitacion"] = tramites
            
        # Extraer votaciones
        votaciones = []
        for votacion in root.findall(".//votaciones/votacion"):
            # Datos básicos de la votación
            votacion_data = {
                # Metadatos de la votación
                "sesion": {
                    "numero": votacion.find("SESION").text.split('/')[0] if votacion.find("SESION") is not None and '/' in votacion.find("SESION").text else None,
                    "legislatura": votacion.find("SESION").text.split('/')[1] if votacion.find("SESION") is not None and '/' in votacion.find("SESION").text else None,
                },
                "fecha": normalize_date(votacion.find("FECHA").text) if votacion.find("FECHA") is not None else None,
                
                # Características de la votación
                "tipo": votacion.find("TIPOVOTACION").text if votacion.find("TIPOVOTACION") is not None else None,
                "quorum": votacion.find("QUORUM").text if votacion.find("QUORUM") is not None else None,
                "etapa": votacion.find("ETAPA").text if votacion.find("ETAPA") is not None else None,
                
                
                # Descripción y contexto
                "descripcion": votacion.find("DESCRIPCION").text if votacion.find("DESCRIPCION") is not None else None,
                "articulo": votacion.find("ARTICULO").text if votacion.find("ARTICULO") is not None else None,
                "tema": votacion.find("TEMA").text if votacion.find("TEMA") is not None else None,
                
                # Conteo general
                "resultado": {
                    "si": int(votacion.find("SI").text) if votacion.find("SI") is not None else None,
                    "no": int(votacion.find("NO").text) if votacion.find("NO") is not None else None,
                    "abstencion": int(votacion.find("ABSTENCION").text) if votacion.find("ABSTENCION") is not None else None,
                    "pareo": int(votacion.find("PAREO").text) if votacion.find("PAREO") is not None else None,
                }
            }
            
            # Detalle de votos por parlamentario
            votos_detalle = []
            
            # Procesar cada tipo de voto
            for voto in votacion.findall(".//VOTO"):
                votos_detalle.append(
                    {
                        "nombre": voto.find("PARLAMENTARIO").text,
                        "voto": voto.find("SELECCION").text
                    }
                )
                        
            # Agregar detalle de votos a la votación
            votacion_data["votos_detalle"] = votos_detalle
            
            # Agregar metadatos adicionales si existen
            if votacion.find("COMISION") is not None:
                votacion_data["comision"] = votacion.find("COMISION").text
                
            if votacion.find("TRAMITE") is not None:
                votacion_data["tramite"] = votacion.find("TRAMITE").text
            
            votaciones.append(votacion_data)
            
        if votaciones:
            proyecto["votaciones"] = votaciones
            
        # Extraer urgencias
        urgencias = []
        for urgencia in root.findall(".//urgencias/urgencia"):
            urgencia_data = {
                "fecha_ingreso": normalize_date(urgencia.find("FECHAINGRESO").text) if urgencia.find("FECHAINGRESO") is not None else None,
                "mensaje_ingreso": urgencia.find("MENSAJEINGRESO").text if urgencia.find("MENSAJEINGRESO") is not None else None,
                "camara_ingreso": urgencia.find("CAMARAINGRESO").text if urgencia.find("CAMARAINGRESO") is not None else None,
                "fecha_retiro": normalize_date(urgencia.find("FECHARETIRO").text) if urgencia.find("FECHARETIRO") is not None else None,
                "mensaje_retiro": urgencia.find("MENSAJERETIRO").text if urgencia.find("MENSAJERETIRO") is not None else None,
                "camara_retiro": urgencia.find("CAMARARETIRO").text if urgencia.find("CAMARARETIRO") is not None else None,
                "tipo": urgencia.find("TIPO").text if urgencia.find("TIPO") is not None else None,
            }
            urgencias.append(urgencia_data)
        if urgencias:
            proyecto["urgencias"] = urgencias
            
        # Extraer informes
        informes = []
        for informe in root.findall(".//informes/informe"):
            informe_data = {
                "fecha": normalize_date(informe.find("FECHAINFORME").text) if informe.find("FECHAINFORME") is not None else None,
                "tramite": informe.find("TRAMITE").text if informe.find("TRAMITE") is not None else None,
                "etapa": informe.find("ETAPA").text if informe.find("ETAPA") is not None else None,
                "link": informe.find("LINK_INFORME").text if informe.find("LINK_INFORME") is not None else None
            }
            informes.append(informe_data)
        if informes:
            proyecto["informes"] = informes
            
        # Extraer oficios
        oficios = []
        for oficio in root.findall(".//oficios/oficio"):
            oficio_data = {
                "numero": oficio.find("NUMERO").text if oficio.find("NUMERO") is not None else None,
                "fecha": normalize_date(oficio.find("FECHA").text) if oficio.find("FECHA") is not None else None,
                "tramite": oficio.find("TRAMITE").text if oficio.find("TRAMITE") is not None else None,
                "etapa": oficio.find("ETAPA").text if oficio.find("ETAPA") is not None else None,
                "tipo": oficio.find("TIPO").text if oficio.find("TIPO") is not None else None,
                "camara": oficio.find("CAMARA").text if oficio.find("CAMARA") is not None else None,
                "descripcion": oficio.find("DESCRIPCION").text if oficio.find("DESCRIPCION") is not None else None,
                "link": oficio.find("LINK_OFICIO").text if oficio.find("LINK_OFICIO") is not None else None
            }
            oficios.append(oficio_data)
        if oficios:
            proyecto["oficios"] = oficios
            
        # Extraer indicaciones
        indicaciones = []
        for indicacion in root.findall(".//indicaciones/indicacion"):
            indicacion_data = {
                "fecha": normalize_date(indicacion.find("FECHA").text) if indicacion.find("FECHA") is not None else None,
                "tramite": indicacion.find("TRAMITE").text if indicacion.find("TRAMITE") is not None else None,
                "etapa": indicacion.find("ETAPA").text if indicacion.find("ETAPA") is not None else None,
                "link": indicacion.find("LINK_INDICACION").text if indicacion.find("LINK_INDICACION") is not None else None
            }
            indicaciones.append(indicacion_data)
        if indicaciones:
            proyecto["indicaciones"] = indicaciones
            
        return proyecto
        
    except ET.ParseError as e:
        logger.error(f"Error parseando XML: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error procesando proyecto: {str(e)}")
        return None

def clean_proyectos(db):
    """
    Limpia y normaliza los datos de proyectos desde raw_proyectos a proyectos_final.
    
    Args:
        db: Conexión a la base de datos MongoDB
    """
    raw_proyectos = db["raw_proyectos"]
    proyectos_final = db["proyectos_final"]
    
    # Crear índice para boletin si no existe
    proyectos_final.create_index("boletin", unique=True)
    
    # Preparar operaciones bulk
    bulk_operations = []
    processed = 0
    errors = 0
    
    for proyecto in raw_proyectos.find():
        try:
            xml_data = proyecto.get("Datos")
            if not xml_data:
                logger.warning(f"Proyecto sin datos XML: {proyecto.get('Boletin')}")
                errors += 1
                continue
                
            # Parsear y normalizar datos
            datos_limpios = parse_proyecto_xml(xml_data)
            if not datos_limpios:
                logger.warning(f"No se pudo parsear el proyecto: {proyecto.get('Boletin')}")
                errors += 1
                continue
            
            # Agregar datos raw para referencia
            datos_limpios["raw_data"] = proyecto
            
            # Crear operación de actualización
            bulk_operations.append(
                UpdateOne(
                    {"boletin": datos_limpios["boletin"]},
                    {"$set": datos_limpios},
                    upsert=True
                )
            )
            
            processed += 1
            
            # Ejecutar en lotes de 1000
            if len(bulk_operations) >= 1000:
                proyectos_final.bulk_write(bulk_operations)
                bulk_operations = []
                logger.info(f"Procesados {processed} proyectos...")
                
        except Exception as e:
            logger.error(f"Error procesando proyecto {proyecto.get('Boletin')}: {str(e)}")
            errors += 1
    
    # Ejecutar operaciones restantes
    if bulk_operations:
        proyectos_final.bulk_write(bulk_operations)
    
    # Logging final
    logger.info(f"Proceso completado: {processed} proyectos procesados, {errors} errores")
    logger.info(f"Total de proyectos en colección final: {proyectos_final.count_documents({})}")
