from django.db import migrations

def crear_permisos_iniciales(apps, schema_editor):
    Permiso = apps.get_model('sst', 'Permiso')
    permisos = [
        # 1️⃣ Usuarios
        "Usuarios Registrados", "Ver usuarios", "Crear usuario", "Modificar usuario", "Habilitar usuario", "Inhabilitar usuario",
        # 2️⃣ Campañas
        "Crear campaña", "Modificar campaña", "Eliminar campaña", "Ver campañas",
        # 3️⃣ Estadísticas
        "Campañas Creadas (para estadísticas)", "Descargar reportes",
        # 4️⃣ Notificaciones
        "Crear notificación", "Modificar notificación", "Eliminar notificación", "Ver notificaciones",
        # 5️⃣ Grupos
        "Crear grupo", "Modificar grupo", "Eliminar grupo", "Ver grupos",
        # 6️⃣ Roles y Permisos
        "Crear rol", "Modificar rol", "Asignar permisos", "Ver roles",
        # 7️⃣ Recursos SST
        "Subir recurso", "Modificar recurso", "Eliminar recurso", "Ver recurso",
        # 8️⃣ Mensajes
        "Enviar mensaje", "Modificar mensaje", "Eliminar mensaje", "Ver mensajes",
        # 9️⃣ Auditoría
        "Ver Logs"
    ]
    for nombre in permisos:
        Permiso.objects.get_or_create(nombre=nombre)

class Migration(migrations.Migration):

    dependencies = [
        ('sst', '0025_remove_permiso_rol_permiso_roles_and_more'),
    ]

    operations = [
        migrations.RunPython(crear_permisos_iniciales),
    ]
