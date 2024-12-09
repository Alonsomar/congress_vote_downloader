from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..utils.db import db
from ..serializers.diputados_serializers import DiputadoSerializer
from ..utils.pagination import StandardResultsSetPagination
from bson import json_util
import json

class DiputadosList(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        # Construir filtros desde query params
        filters = {}
        
        # Filtrar por nombre
        if nombre := request.query_params.get('nombre'):
            filters['nombre_completo'] = {'$regex': nombre, '$options': 'i'}
            
        # Filtrar por sexo
        if sexo := request.query_params.get('sexo'):
            filters['sexo'] = sexo.upper()

        # Obtener total de documentos
        total = db["diputados_final"].count_documents(filters)
        
        # Aplicar paginación
        paginator = self.pagination_class()
        page_size = paginator.get_page_size(request)
        page = int(request.query_params.get('page', 1))
        skip = (page - 1) * page_size

        # Consultar con paginación
        diputados = list(db["diputados_final"]
                        .find(filters, {"_id": 0, "raw_data": 0})
                        .skip(skip)
                        .limit(page_size))

        # Serializar
        serializer = DiputadoSerializer(diputados, many=True)
        
        return Response({
            'count': total,
            'next': page * page_size < total,
            'previous': page > 1,
            'results': serializer.data
        })


class DiputadoDetail(APIView):
    def get(self, request, dipid):
        diputado = db["diputados_final"].find_one({"DIPID": dipid}, {"_id": 0, "raw_data": 0})
        if not diputado:
            return Response({"detail": "Diputado no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiputadoSerializer(diputado)
        return Response(serializer.data, status=status.HTTP_200_OK)
