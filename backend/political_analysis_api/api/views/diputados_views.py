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
        filters = {}
        
        if nombre := request.query_params.get('nombre'):
            filters['nombre_completo'] = {'$regex': nombre, '$options': 'i'}
        if sexo := request.query_params.get('sexo'):
            filters['sexo'] = sexo.upper()
        if region := request.query_params.get('region'):
            filters['region'] = region
        if partido := request.query_params.get('partido'):
            filters['partido'] = partido
        if comision := request.query_params.get('comision'):
            filters['comisiones'] = comision
        
        # Sorting
        sort_by = request.query_params.get('sort_by', 'nombre')
        sort_field = {
            'nombre': 'nombre_completo',
            'partido': 'partido',
            'region': 'region',
            'asistencia': 'asistencia'
        }.get(sort_by, 'nombre_completo')
        
        # Get page size
        page_size = int(request.query_params.get('page_size', 20))
        page = int(request.query_params.get('page', 1))
        skip = (page - 1) * page_size

        # Query with sorting
        diputados = list(db["diputados_final"]
                        .find(filters)
                        .sort([(sort_field, 1)])
                        .skip(skip)
                        .limit(page_size))

        # Serializar
        serializer = DiputadoSerializer(diputados, many=True)
        
        return Response({
            'count': len(diputados),
            'next': page * page_size < len(diputados),
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

class DiputadosStats(APIView):
    def get(self, request):
        total = db["diputados_final"].count_documents({})
        mujeres = db["diputados_final"].count_documents({"sexo": "F"})
        
        # Calcular asistencia promedio
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "asistenciaPromedio": {"$avg": "$asistencia"}
                }
            }
        ]
        asistencia_result = list(db["diputados_final"].aggregate(pipeline))
        asistencia_promedio = round(asistencia_result[0].get("asistenciaPromedio", 0) or 0, 2)
        
        # Contar proyectos presentados
        proyectos = db["diputados_final"].aggregate([
            {"$unwind": "$proyectos"},
            {"$group": {"_id": None, "total": {"$sum": 1}}}
        ])
        proyectos_total = next(proyectos, {"total": 0})["total"]

        return Response({
            "total": total,
            "mujeres": mujeres,
            "asistenciaPromedio": asistencia_promedio,
            "proyectosPresentados": proyectos_total
        })

class DiputadosOptions(APIView):
    def get(self, request):
        # Obtener opciones únicas de la base de datos
        partidos = db["diputados_final"].distinct("partido")
        regiones = db["diputados_final"].distinct("region")
        comisiones = db["diputados_final"].distinct("comisiones")
        
        return Response({
            "partidos": [p for p in partidos if p],  # Filtrar valores nulos
            "regiones": [r for r in regiones if r],
            "comisiones": [c for c in comisiones if c]
        })
