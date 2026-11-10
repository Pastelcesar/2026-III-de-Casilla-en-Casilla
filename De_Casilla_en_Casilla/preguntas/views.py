from django.shortcuts import render




from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Pregunta

#
class SoloCreadoresMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol in ['admin', 'creador']


class PreguntaListView(ListView):
    model = Pregunta
    template_name = 'preguntas/lista.html'
    context_object_name = 'preguntas'

    
class PreguntaCreateView(LoginRequiredMixin, SoloCreadoresMixin, CreateView):
    model = Pregunta
    fields = ['texto', 'respuesta_correcta', 'respuesta_incorrecta_1', 'respuesta_incorrecta_2']
    template_name = 'preguntas/formulario.html'
    success_url = reverse_lazy('lista_preguntas')


    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PreguntaUpdateView(LoginRequiredMixin, SoloCreadoresMixin, UpdateView):
    model = Pregunta
    fields = ['texto', 'respuesta_correcta', 'respuesta_incorrecta_1', 'respuesta_incorrecta_2']
    template_name = 'preguntas/formulario.html'
    success_url = reverse_lazy('lista_preguntas')