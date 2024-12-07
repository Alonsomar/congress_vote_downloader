from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def status(request):
    return Response({'status': 'ok'}, status=200)
