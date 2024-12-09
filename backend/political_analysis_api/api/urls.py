from django.urls import path
from .views.root_view import APIRoot
from .views.diputados_views import DiputadosList, DiputadoDetail
from .views.proyectos_views import ProyectosList, ProyectoDetail

urlpatterns = [
    path('', APIRoot.as_view(), name='api-root'),
    path('diputados/', DiputadosList.as_view(), name='diputados-list'),
    path('diputados/<str:dipid>/', DiputadoDetail.as_view(), name='diputado-detail'),
    path('proyectos/', ProyectosList.as_view(), name='proyectos-list'),
    path('proyectos/<str:boletin>/', ProyectoDetail.as_view(), name='proyecto-detail'),
]
