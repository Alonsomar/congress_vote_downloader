from datetime import datetime
import re

def normalize_date(date_str):
    """
    Normaliza fechas a formato ISO8601 (YYYY-MM-DD).
    
    Args:
        date_str (str): Fecha en formato string
        
    Returns:
        str: Fecha en formato ISO8601 o None si no se puede parsear
    """
    if not date_str:
        return None
        
    # Patrones comunes de fecha
    patterns = [
        "%Y-%m-%d",  # 2020-12-31
        "%d/%m/%Y",  # 31/12/2020
        "%Y/%m/%d",  # 2020/12/31
        "%d-%m-%Y"   # 31-12-2020
    ]
    
    for pattern in patterns:
        try:
            return datetime.strptime(date_str.strip(), pattern).strftime("%d/%m/%Y")
        except ValueError:
            continue
    
    return None

def normalize_name(name):
    """
    Normaliza nombres eliminando espacios extras y caracteres especiales.
    
    Args:
        name (str): Nombre a normalizar
        
    Returns:
        str: Nombre normalizado
    """
    if not name:
        return ""
    
    # Eliminar espacios múltiples y caracteres especiales
    name = re.sub(r'\s+', ' ', name.strip())
    # Convertir primera letra de cada palabra a mayúscula
    return " ".join(word.capitalize() for word in name.split())

def normalize_gender(gender):
    """
    Normaliza el género a un formato estándar.
    
    Args:
        gender (str): Género a normalizar
        
    Returns:
        str: 'M' para masculino, 'F' para femenino, None si no se puede determinar
    """
    if not gender:
        return None
        
    gender = gender.upper().strip()
    if gender in ['M', 'MASCULINO', 'HOMBRE', 'H']:
        return 'M'
    elif gender in ['F', 'FEMENINO', 'MUJER', 'M']:
        return 'F'
    return None
