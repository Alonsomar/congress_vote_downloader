from rest_framework import serializers
from datetime import datetime
import re

class ProyectoSerializer(serializers.Serializer):
    boletin = serializers.CharField()
    titulo = serializers.CharField(allow_null=True)
    estado = serializers.CharField(allow_null=True)
    etapa = serializers.CharField(allow_null=True)
    subetapa = serializers.CharField(allow_null=True)
    urgencia_actual = serializers.CharField(allow_null=True)
    fecha_ingreso = serializers.DateTimeField(allow_null=True)
    iniciativa = serializers.CharField(allow_null=True)
    camara_origen = serializers.CharField(allow_null=True)
    link_mensaje_mocion = serializers.CharField(allow_null=True)
    ley = serializers.DictField(required=False)
    refundidos = serializers.ListField(child=serializers.CharField(), required=False)
    autores = serializers.ListField(child=serializers.CharField(), required=False)
    materias = serializers.ListField(child=serializers.CharField(), required=False)
    tramitacion = serializers.ListField(required=False)
    votaciones = serializers.ListField(required=False)
    urgencias = serializers.ListField(required=False)
    informes = serializers.ListField(required=False)
    oficios = serializers.ListField(required=False)
    indicaciones = serializers.ListField(required=False)

    def validate_boletin(self, value):
        if not value:
            raise serializers.ValidationError("El boletín no puede estar vacío")
        # Validar formato de boletín (ejemplo: ####-##)
        if not re.match(r'^\d{4}-\d{2}$', value):
            raise serializers.ValidationError("Formato de boletín inválido")
        return value

    def validate_fecha_ingreso(self, value):
        if value and value > datetime.now():
            raise serializers.ValidationError("La fecha de ingreso no puede ser futura")
        return value
