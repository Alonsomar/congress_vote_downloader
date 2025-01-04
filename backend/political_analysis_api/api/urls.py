from django.urls import path
from .views.root_view import APIRoot
from .views.diputados_views import DiputadosList, DiputadoDetail, DiputadosStats, DiputadosOptions
from .views.proyectos_views import ProyectosList, ProyectoDetail

urlpatterns = [
    path('', APIRoot.as_view(), name='api-root'),
    path('diputados/stats/', DiputadosStats.as_view()),
    path('diputados/options/', DiputadosOptions.as_view()),
    path('diputados/<str:dipid>/', DiputadoDetail.as_view()),
    path('diputados/', DiputadosList.as_view()),
    path('proyectos/', ProyectosList.as_view(), name='proyectos-list'),
    path('proyectos/<str:boletin>/', ProyectoDetail.as_view(), name='proyecto-detail'),
]
