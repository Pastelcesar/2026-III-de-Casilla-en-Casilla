import random
from django.conf import settings
from django.db import models



class Nivel(models.Model):
   
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Nivel")
    descripcion = models.TextField(verbose_name="Descripción y público objetivo (edades)")

    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="niveles_creados")

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name="preguntas")
    
    texto = models.CharField(max_length=500, verbose_name="Pregunta")
    respuesta_correcta = models.CharField(max_length=255)
    respuesta_incorrecta_1 = models.CharField(max_length=255)
    respuesta_incorrecta_2 = models.CharField(max_length=255)

    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        return f"[{self.nivel.nombre}] {self.texto}"

  
    def obtener_respuestas_aleatorias(self):
        respuestas = [
            self.respuesta_correcta,
            self.respuesta_incorrecta_1,
            self.respuesta_incorrecta_2
        ]
        random.shuffle(respuestas)
        return respuestas


    
   