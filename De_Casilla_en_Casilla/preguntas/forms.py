from django import forms
from .models import Pregunta

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['nivel', 'texto_pregunta', 'casillas_avanza', 'casillas_retrocede']
     