from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Usuario

def aplicar_estilos_bootstrap(form):
    """Aplica las clases de Bootstrap a todos los campos del formulario automáticamente"""
    for field_name, field in form.fields.items():
        if isinstance(field.widget, forms.Select):
            field.widget.attrs['class'] = 'form-select'
        elif isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs['class'] = 'form-check-input'
        else:
            field.widget.attrs['class'] = 'form-control'

class RegistroPublicoForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self)
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['username'].help_text = '' # Quitamos el texto de ayuda largo de Django
        self.fields['email'].widget.attrs['placeholder'] = 'Correo electrónico'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Teléfono'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'

class UsuarioAdminCreationForm(UserCreationForm):
    """Formulario para que el Admin CREE un usuario desde cero en el panel"""
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            'username',
            'email',
            'telefono',
            'puede_ver_panel_usuarios',
            'puede_crear_usuarios',
            'puede_administrar_usuarios',
            'puede_crear_preguntas',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self)
        self.fields['username'].help_text = ''


class UsuarioUpdateForm(forms.ModelForm):
    """Formulario para que el Admin EDITE un usuario existente"""
    class Meta:
        model = Usuario

        fields = (
            'username',
            'email',
            'telefono',
            'is_active',
            'puede_ver_panel_usuarios',
            'puede_crear_usuarios',
            'puede_administrar_usuarios',
            'puede_crear_preguntas',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self) 


class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'codename', 'content_type']
        labels = {
            'name': 'Nombre del Permiso',
            'codename': 'Código (Codename)',
            'content_type': 'Módulo Asociado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_estilos_bootstrap(self)
        
        self.fields['content_type'].queryset = ContentType.objects.all()

        traducciones = {
            'user': 'Módulo de Usuario',
            'usuario': 'Módulo de Usuarios',
            'permission': 'Módulo de Permisos',
            'group': 'Módulo de Grupos',
            'session': 'Módulo de Sesiones',
            'logentry': 'Módulo de Administración',
            'contenttype': 'Tipos de Contenido',
        }

        self.fields['content_type'].label_from_instance = lambda obj: traducciones.get(
            obj.model.lower(),
            f"Módulo de {obj.model.capitalize()}"
        )