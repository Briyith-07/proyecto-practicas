from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from sst.models import CampanaAsignada, Notificacion


def enviar_recordatorio(usuario, campaña):
    """
    Envía un recordatorio por correo y crea una notificación web.
    """
    # --- Correo ---
    asunto = f"Recordatorio: Pausa activa {campaña.nombre}"
    mensaje = f"Hola {usuario.first_name}, tienes una pausa activa pendiente: {campaña.nombre}.\n\nDetalle: {campaña.detalle}"
    correo_destino = usuario.email

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [correo_destino],
        fail_silently=False
    )

    # --- Notificación web ---
    Notificacion.objects.create(
        campaña=campaña,
        usuario=usuario,
        cedula=usuario.cedula,
        titulo=f"Recordatorio: {campaña.nombre}",
        mensaje=f"Hola {usuario.first_name}, tienes una pausa activa pendiente.",
        tipo='web',
        enviada=True
    )


class Command(BaseCommand):
    help = 'Enviar recordatorios de pausas activas'

    def handle(self, *args, **kwargs):
        ahora = timezone.localtime(timezone.now())

        # Filtrar asignaciones activas y no realizadas
        asignaciones = CampanaAsignada.objects.filter(
            realizada=False,
            campaña__estado='activa'
        )

        for asign in asignaciones:
            # Solo si la campaña tiene horario definido
            if asign.campaña.horarios:
                # Convertimos el string "08:00" en hora
                try:
                    horario_inicio = timezone.datetime.strptime(
                        asign.campaña.horarios.split(" - ")[0], "%H:%M"
                    ).time()
                except:
                    continue

                # Recordatorio 10 minutos antes
                delta = timezone.timedelta(minutes=10)
                if ahora.time() >= (timezone.datetime.combine(ahora.date(), horario_inicio) - delta).time() \
                   and ahora.time() <= horario_inicio:
                    enviar_recordatorio(asign.empleado, asign.campaña)
                    self.stdout.write(
                        f'Recordatorio enviado a {asign.empleado.email} para {asign.campaña.nombre}'
                    )
