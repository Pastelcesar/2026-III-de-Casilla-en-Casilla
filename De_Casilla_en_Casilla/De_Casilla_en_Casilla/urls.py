from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('preguntas/', include('preguntas.urls')),
    path('auth/', include('usuarios.urls')),
]