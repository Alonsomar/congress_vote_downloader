from rest_framework import serializers

class DiputadoSerializer(serializers.Serializer):
    DIPID = serializers.CharField()
    nombre = serializers.CharField()
    apellido_paterno = serializers.CharField()
    apellido_materno = serializers.CharField()
    nombre_completo = serializers.CharField()
    fecha_nacimiento = serializers.DateTimeField(allow_null=True)
    sexo = serializers.CharField(allow_null=True)
    