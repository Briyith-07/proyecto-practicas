from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import CampanaAsignada, Notificacion, RecursoSSTAdmin, RecursoSSTEmpleado
from .models import Mensaje, Usuario,EvidenciaCampaña

@receiver(post_save, sender=CampanaAsignada)
def notificar_asignacion_campaña(sender, instance, created, **kwargs):
    if created and instance.empleado:

        campaña = instance.campaña
        asignacion = instance

        # Datos seguros
        nombre_campaña = campaña.codigo.nombre if campaña.codigo else "Sin nombre"
        codigo_campaña = campaña.codigo.codigo if campaña.codigo else "N/A"
        fecha_creacion = campaña.fecha_creacion.strftime("%d/%m/%Y")
        periodicidad = campaña.periodicidad or "No definida"

        fecha_vencimiento = (
            asignacion.fecha_vencimiento.strftime("%d/%m/%Y")
            if asignacion.fecha_vencimiento else "Sin fecha"
        )

        # ===============================
        # 🔔 NOTIFICACIÓN WEB
        # ===============================
        titulo = "📢 Nueva Campaña Asignada"
        mensaje = (
            f"Se te ha asignado una nueva campaña:\n\n"
            f"📌 *Detalles de la campaña*\n"
            f"• **Nombre:** {nombre_campaña}\n"
            f"• **Código:** {codigo_campaña}\n"
            f"• **Periodicidad:** {periodicidad}\n"
            f"• **Fecha de creación:** {fecha_creacion}\n"
            f"• **Fecha de vencimiento:** {fecha_vencimiento}\n\n"
            f"Por favor ingresa al sistema para revisar los detalles."
        )

        Notificacion.objects.create(
            campaña=campaña,
            usuario=instance.empleado,
            cedula=instance.empleado.cedula,
            titulo=titulo,
            mensaje=mensaje,
            tipo="web",
            enviada=True,
        )

        # ===============================
        # ✉️ CORREO ELECTRÓNICO HTML
        # ===============================
        if instance.empleado.email:

            subject = "📢 Nueva Campaña Asignada"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [instance.empleado.email]

            # Texto plano para compatibilidad
            text_content = (
                f"Hola {instance.empleado.first_name},\n\n"
                f"Has recibido una nueva campaña asignada.\n"
                f"Nombre: {nombre_campaña}\n"
                f"Código: {codigo_campaña}\n"
                f"Periodicidad: {periodicidad}\n"
                f"Fecha de creación: {fecha_creacion}\n"
                f"Fecha de vencimiento: {fecha_vencimiento}\n"
            )

            # HTML con diseño
            html_content = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
                <p>Hola <strong>{instance.empleado.first_name}</strong>,</p>

                <p>Has recibido una nueva campaña asignada. Aquí tienes los detalles:</p>

                <h3 style="color:#0044cc;">📌 Detalles de la campaña</h3>

                <ul style="font-size: 15px; line-height: 1.6;">
                    <li><strong>Nombre:</strong> {nombre_campaña}</li>
                    <li><strong>Código:</strong> {codigo_campaña}</li>
                    <li><strong>Periodicidad:</strong> {periodicidad}</li>
                    <li><strong>Fecha de creación:</strong> {fecha_creacion}</li>
                    <li><strong>Fecha de vencimiento:</strong> {fecha_vencimiento}</li>
                </ul>

                <p>Por favor revisa el sistema para más información.</p>

                <p style="margin-top: 30px; color: #555;"> <em>© 2025 SG-SST Sistema de Seguridad y salud en el Trabajo y Pausas Activas</em></p>
            </div>
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@receiver(post_save, sender=RecursoSSTAdmin)
def crear_recurso_empleado(sender, instance, created, **kwargs):
    if created:
        RecursoSSTEmpleado.objects.create(recurso=instance, visible=True)


@receiver(post_save, sender=Mensaje)
def enviar_correo_mensaje_empleado(sender, instance, created, **kwargs):
    if created:
        empleados = Usuario.objects.filter(rol__nombre='empleado')
        for empleado in empleados:
            subject = f"📢 Nuevo mensaje: {instance.titulo}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [empleado.email]

            # Texto plano
            text_content = f"Hola {empleado.first_name},\n\n{instance.contenido}"
            if instance.fecha_evento:
                text_content += f"\n📅 Fecha del evento: {instance.fecha_evento.strftime('%d/%m/%Y %H:%M')}"

            # HTML
            html_content = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
                <p>Hola <strong>{empleado.first_name}</strong>,</p>

                <p>Has recibido un nuevo mensaje. Aquí tienes los detalles:</p>

                <h3 style="color:#0044cc;">📌 Detalles del mensaje</h3>
                <ul style="font-size: 15px; line-height: 1.6;">
                    <li><strong>Asunto:</strong> {instance.titulo}</li>
                    <li><strong>Contenido:</strong> {instance.contenido}</li>
                    <li><strong>Fecha de creación:</strong> {instance.creado.strftime('%d/%m/%Y')}</li>
            """

            # Agregar fecha y hora del evento si existe
            if instance.fecha_evento:
                html_content += f"<li><strong>Fecha del evento:</strong> {instance.fecha_evento.strftime('%d/%m/%Y %H:%M')}</li>"

            html_content += """
                </ul>
                <p style="margin-top: 30px; color: #555;"> 
                    <em>© 2025 SG-SST Sistema de Seguridad y salud en el Trabajo y Pausas Activas</em>
                </p>
            </div>
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()



# ============================================
# 🔔 Notificar al ADMIN cuando un empleado sube evidencia
# ============================================
@receiver(post_save, sender=EvidenciaCampaña)
def notificar_evidencia_subida(sender, instance, created, **kwargs):

    campaña = instance.campaña
    empleado = instance.empleado

    # Buscar administradores
    administradores = Usuario.objects.filter(rol__nombre="Administrador")
    if not administradores.exists():
        return  

    # Notificación en campana
    for admin in administradores:
        Notificacion.objects.create(
            campaña=campaña,
            usuario=admin,
            remitente=empleado,
            cedula=empleado.cedula,
            titulo="📥 Nueva evidencia subida",
            mensaje=(
                f"El empleado **{empleado.first_name} {empleado.last_name}** ha subido "
                f"una evidencia para la campaña **{campaña.nombre}**.\n\n"
                f"Por favor revisa y aprueba o rechaza la evidencia."
            ),
            tipo="web",
            enviada=True,
        )

    # Enviar correo
    for admin in administradores:
        if admin.email:
            subject = "📥 Nueva evidencia pendiente de aprobación"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [admin.email]

            text_content = (
                f"Hola {admin.first_name},\n\n"
                f"El empleado {empleado.first_name} {empleado.last_name} ha subido "
                f"una evidencia para la campaña: {campaña.nombre}.\n\n"
                f"Por favor ingresa al sistema para revisarla."
            )

            html_content = f"""
            <div style="font-family: Arial; padding: 20px; color: #333;">
                <h2 style="color:#0044cc;">📥 Nueva evidencia subida</h2>
                <p>El empleado <strong>{empleado.first_name} {empleado.last_name}</strong> ha cargado evidencia
                para la campaña <strong>{campaña.nombre}</strong>.</p>
                <p>Por favor revisa la evidencia y aprueba o rechaza según corresponda.</p>
                <p style="margin-top: 25px; color:#777">
                    © 2025 SG-SST Sistema de Seguridad y salud en el Trabajo y Pausas Activas
                </p>
            </div>
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()