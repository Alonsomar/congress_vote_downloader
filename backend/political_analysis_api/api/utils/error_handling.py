from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from pymongo.errors import PyMongoError
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Llamar primero al manejador por defecto
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, PyMongoError):
            logger.error(f"Error de MongoDB: {str(exc)}")
            return Response({
                'error': 'Error en la base de datos',
                'detail': str(exc)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Log del error no manejado
        logger.error(f"Error no manejado: {str(exc)}")
        return Response({
            'error': 'Error interno del servidor',
            'detail': str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response 