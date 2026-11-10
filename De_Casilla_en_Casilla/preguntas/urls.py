from django.urls import path
from . import views


urlpatterns = [
     path('', views.PreguntaListView.as_view(), name='lista_preguntas'),
    path('nueva/', views.PreguntaCreateView.as_view(), name='crear_pregunta'),
    path('<int:pk>/editar/', views.PreguntaUpdateView.as_view(), name='editar_pregunta'),
    
]
