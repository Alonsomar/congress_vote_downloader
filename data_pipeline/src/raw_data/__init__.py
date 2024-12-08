"""
Raw data collection module for the Congressional data pipeline.

This module provides functions to fetch raw data from various congressional sources.
"""

from raw_data.get_asistencia import main as get_asistencia
from raw_data.get_periodos import main as get_periodos
from raw_data.get_diputados_periodo import main as get_diputados_periodo
from raw_data.get_sesiones import main as get_sesiones
from raw_data.get_boletin import main as get_boletin
from raw_data.get_proyectos import main as get_proyectos
from raw_data.get_votaciones import main as get_votaciones
from raw_data.get_votacion_detalle import main as get_votacion_detalle
from raw_data.get_legislaturas import main as get_legislaturas

__all__ = [
    'get_legislaturas',
    'get_asistencia',
    'get_periodos',
    'get_diputados_periodo',
    'get_sesiones',
    'get_boletin',
    'get_proyectos',
    'get_votaciones',
    'get_votacion_detalle'
]