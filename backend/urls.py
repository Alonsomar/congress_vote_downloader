from django.urls import path
from .api.views import status

urlpatterns = [
    path('api/status', status, name='status')
]
