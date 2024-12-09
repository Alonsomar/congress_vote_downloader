from django.core.cache import cache 
from functools import wraps
import hashlib
import json
from rest_framework.response import Response

def cache_response(timeout=300):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            # Crear key única basada en la URL y parámetros
            cache_key = f"{request.path}:{json.dumps(request.query_params)}"
            cache_key = hashlib.md5(cache_key.encode()).hexdigest()

            # Intentar obtener del cache
            response_data = cache.get(cache_key)
            
            if response_data is None:
                response = view_func(self, request, *args, **kwargs)
                cache.set(cache_key, response.data, timeout)
                return response
                
            return Response(response_data)
        return wrapper
    return decorator 