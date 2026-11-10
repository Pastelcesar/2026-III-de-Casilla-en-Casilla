from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PreguntaForm
from .models import Pregunta


class SoloCreadoresMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_superuser or user.puede_crear_preguntas
        )


class PreguntaListView(LoginRequiredMixin, ListView):
    model = Pregunta
    template_name = 'preguntas/lista.html'
    context_object_name = 'preguntas'

    def get_queryset(self):
        return super().get_queryset().select_related('nivel', 'autor').order_by('nivel__nombre', 'texto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['puede_editar_preguntas'] = (
            user.is_superuser or user.puede_crear_preguntas
        )
        return context


class PreguntaCreateView(LoginRequiredMixin, SoloCreadoresMixin, CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'preguntas/crear.html'
    success_url = reverse_lazy('lista_preguntas')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PreguntaUpdateView(LoginRequiredMixin, SoloCreadoresMixin, UpdateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'preguntas/crear.html'
    success_url = reverse_lazy('lista_preguntas')


class PreguntaDeleteView(LoginRequiredMixin, SoloCreadoresMixin, DeleteView):
    model = Pregunta
    template_name = 'preguntas/eliminar.html'
    success_url = reverse_lazy('lista_preguntas')