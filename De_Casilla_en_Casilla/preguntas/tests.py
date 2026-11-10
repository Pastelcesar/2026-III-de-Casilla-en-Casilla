from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Nivel, Pregunta


class PreguntasViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.creador = user_model.objects.create_user(
            username='creador',
            password='test-password',
            rol='creador',
            puede_crear_preguntas=True,
        )
        self.jugador = user_model.objects.create_user(
            username='jugador',
            password='test-password',
            rol='jugador',
        )
        self.nivel = Nivel.objects.create(
            nombre='Primaria',
            descripcion='Preguntas para primaria',
            creador=self.creador,
        )
        self.pregunta = Pregunta.objects.create(
            nivel=self.nivel,
            texto='¿Cuánto es 2 + 2?',
            respuesta_correcta='4',
            respuesta_incorrecta_1='3',
            respuesta_incorrecta_2='5',
            autor=self.creador,
        )

    def test_questions_list_requires_login(self):
        response = self.client.get(reverse('lista_preguntas'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('lista_preguntas')}",
        )

    def test_logged_in_user_sees_question_fields(self):
        self.client.force_login(self.jugador)

        response = self.client.get(reverse('lista_preguntas'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pregunta.texto)
        self.assertContains(response, self.pregunta.respuesta_correcta)
        self.assertContains(response, self.pregunta.respuesta_incorrecta_1)
        self.assertContains(response, self.pregunta.respuesta_incorrecta_2)
        self.assertContains(response, self.nivel.nombre)
        self.assertNotContains(response, reverse('crear_pregunta'))

    def test_creator_can_create_question(self):
        self.client.force_login(self.creador)

        response = self.client.post(
            reverse('crear_pregunta'),
            {
                'nivel': self.nivel.pk,
                'texto': '¿Capital de México?',
                'respuesta_correcta': 'Ciudad de México',
                'respuesta_incorrecta_1': 'Guadalajara',
                'respuesta_incorrecta_2': 'Monterrey',
            },
        )

        self.assertRedirects(response, reverse('lista_preguntas'))
        pregunta = Pregunta.objects.get(texto='¿Capital de México?')
        self.assertEqual(pregunta.autor, self.creador)

    def test_creator_can_delete_question(self):
        self.client.force_login(self.creador)

        response = self.client.post(
            reverse('eliminar_pregunta', args=[self.pregunta.pk])
        )

        self.assertRedirects(response, reverse('lista_preguntas'))
        self.assertFalse(Pregunta.objects.filter(pk=self.pregunta.pk).exists())

    def test_player_cannot_create_or_delete_questions(self):
        self.client.force_login(self.jugador)

        create_response = self.client.get(reverse('crear_pregunta'))
        delete_response = self.client.get(
            reverse('eliminar_pregunta', args=[self.pregunta.pk])
        )

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_legacy_creator_role_without_permission_cannot_create_questions(self):
        self.creador.puede_crear_preguntas = False
        self.creador.save(update_fields=['puede_crear_preguntas'])
        self.client.force_login(self.creador)

        response = self.client.get(reverse('crear_pregunta'))

        self.assertEqual(response.status_code, 403)
