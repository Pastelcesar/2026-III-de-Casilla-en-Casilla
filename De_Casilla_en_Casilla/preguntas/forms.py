from django import forms
from .models import Pregunta

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = [
            'nivel',
            'texto',
            'respuesta_correcta',
            'respuesta_incorrecta_1',
            'respuesta_incorrecta_2',
        ]