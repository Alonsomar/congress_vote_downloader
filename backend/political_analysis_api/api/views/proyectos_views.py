from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..utils.db import db
from ..serializers.proyectos_serializers import ProyectoSerializer
from ..utils.pagination import StandardResultsSetPagination
from ..utils.cache import cache_response
from datetime import datetime

class ProyectosList(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        # Construir query de búsqueda
        query = {}
        
        # Filtros básicos
        if titulo := request.GET.get('titulo'):
            query['titulo'] = {'$regex': titulo, '$options': 'i'}
            
        if estado := request.GET.get('estado'):
            query['estado'] = {'$regex': f'^{estado}$', '$options': 'i'}
            
        # Filtro por fecha
        fecha_desde = request.GET.get('fecha_desde')
        fecha_hasta = request.GET.get('fecha_hasta')
        if fecha_desde or fecha_hasta:
            query['fecha_ingreso'] = {}
            if fecha_desde:
                query['fecha_ingreso']['$gte'] = datetime.fromisoformat(fecha_desde)
            if fecha_hasta:
                query['fecha_ingreso']['$lte'] = datetime.fromisoformat(fecha_hasta)
                
        # Filtro por materias y autores (pueden ser múltiples)
        if materias := request.GET.getlist('materias'):
            query['materias'] = {'$in': materias}
            
        if autores := request.GET.getlist('autores'):
            query['autores'] = {'$in': autores}

        # Obtener parámetros de paginación
        paginator = self.pagination_class()
        page_size = paginator.get_page_size(request)
        page = int(request.GET.get('page', 1))
        skip = (page - 1) * page_size

        # Obtener total y proyectos paginados
        total = db["proyectos_final"].count_documents(query)
        proyectos = list(db["proyectos_final"]
                        .find(query, {"_id": 0, "raw_data": 0})
                        .skip(skip)
                        .limit(page_size))

        serializer = ProyectoSerializer(proyectos, many=True)
        
        return Response({
            'count': total,
            'next': page * page_size < total,
            'previous': page > 1,
            'results': serializer.data
        })

class ProyectoDetail(APIView):
    def get(self, request, boletin):
        proyecto = db["proyectos_final"].find_one({"boletin": boletin}, {"_id": 0, "raw_data": 0})
        if not proyecto:
            return Response({"detail": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProyectoSerializer(proyecto)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProyectosSearch(APIView):
    pagination_class = StandardResultsSetPagination

    @cache_response(timeout=300)
    def post(self, request):
        # Construir query de búsqueda
        query = {}
        
        # Filtros básicos
        if titulo := request.data.get('titulo'):
            query['titulo'] = {'$regex': titulo, '$options': 'i'}
            
        if estado := request.data.get('estado'):
            query['estado'] = {'$regex': f'^{estado}$', '$options': 'i'}
            
        # Filtro por fecha
        fecha_desde = request.data.get('fecha_desde')
        fecha_hasta = request.data.get('fecha_hasta')
        if fecha_desde or fecha_hasta:
            query['fecha_ingreso'] = {}
            if fecha_desde:
                query['fecha_ingreso']['$gte'] = datetime.fromisoformat(fecha_desde)
            if fecha_hasta:
                query['fecha_ingreso']['$lte'] = datetime.fromisoformat(fecha_hasta)
                
        # Filtro por materias
        if materias := request.data.get('materias'):
            query['materias'] = {'$in': materias}
            
        # Filtro por autores
        if autores := request.data.get('autores'):
            query['autores'] = {'$in': autores}

        # Aplicar paginación
        paginator = self.pagination_class()
        page_size = paginator.get_page_size(request)
        page = int(request.data.get('page', 1))
        skip = (page - 1) * page_size

        # Ejecutar búsqueda
        total = db["proyectos_final"].count_documents(query)
        proyectos = list(db["proyectos_final"]
                        .find(query, {"_id": 0, "raw_data": 0})
                        .skip(skip)
                        .limit(page_size))

        serializer = ProyectoSerializer(proyectos, many=True)
        
        return Response({
            'count': total,
            'next': page * page_size < total,
            'previous': page > 1,
            'results': serializer.data
        })
