from django.db import migrations, models


def asignar_permisos_por_rol(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    usuarios = Usuario.objects.using(schema_editor.connection.alias)
    permisos_por_rol = {
        'admin': {
            'puede_ver_panel_usuarios': True,
            'puede_crear_usuarios': True,
            'puede_administrar_usuarios': True,
            'puede_crear_preguntas': True,
        },
        'lectura': {
            'puede_ver_panel_usuarios': True,
        },
        'creador': {
            'puede_ver_panel_usuarios': True,
            'puede_crear_usuarios': True,
        },
    }

    for rol, permisos in permisos_por_rol.items():
        usuarios.filter(rol=rol).update(**permisos)


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuario_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='puede_ver_panel_usuarios',
            field=models.BooleanField(default=False, verbose_name='Ver panel de usuarios'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='puede_crear_usuarios',
            field=models.BooleanField(default=False, verbose_name='Crear usuarios'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='puede_administrar_usuarios',
            field=models.BooleanField(default=False, verbose_name='Editar y eliminar usuarios'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='puede_crear_preguntas',
            field=models.BooleanField(default=False, verbose_name='Crear, editar y eliminar preguntas'),
        ),
        migrations.RunPython(asignar_permisos_por_rol, migrations.RunPython.noop),
    ]
