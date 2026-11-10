from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UsuarioPermisosTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_user(
            username='administrador',
            password='test-password',
            puede_ver_panel_usuarios=True,
            puede_crear_usuarios=True,
            puede_administrar_usuarios=True,
        )
        self.usuario = user_model.objects.create_user(
            username='alumno',
            password='test-password',
        )
        self.client.force_login(self.admin)

    def test_user_edit_form_displays_multiple_permission_checkboxes(self):
        response = self.client.get(
            reverse('panel_usuario_editar', args=[self.usuario.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="puede_crear_usuarios"')
        self.assertContains(response, 'name="puede_crear_preguntas"')

    def test_admin_can_assign_multiple_permissions_to_user(self):
        response = self.client.post(
            reverse('panel_usuario_editar', args=[self.usuario.pk]),
            {
                'username': self.usuario.username,
                'email': self.usuario.email,
                'telefono': '',
                'is_active': 'on',
                'puede_crear_usuarios': 'on',
                'puede_crear_preguntas': 'on',
            },
        )

        self.assertRedirects(response, reverse('panel_usuarios_lista'))
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.puede_crear_usuarios)
        self.assertTrue(self.usuario.puede_crear_preguntas)

    def test_user_panel_has_create_question_button_for_question_permission(self):
        self.admin.puede_crear_preguntas = True
        self.admin.save(update_fields=['puede_crear_preguntas'])

        response = self.client.get(reverse('panel_usuarios_lista'))

        self.assertContains(response, 'Crear pregunta')
        self.assertContains(response, reverse('crear_pregunta'))
