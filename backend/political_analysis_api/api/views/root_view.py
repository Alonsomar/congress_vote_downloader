from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

class APIRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'diputados': reverse('diputados-list', request=request, format=format),
            'proyectos': reverse('proyectos-list', request=request, format=format),
            'docs': reverse('schema-swagger-ui', request=request, format=format),
        }) 