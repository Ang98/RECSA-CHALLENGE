import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppointmentConfig(AppConfig):
    name = "recsa_challenge.appointments"
    verbose_name = _("Appointments")

    def ready(self):
        with contextlib.suppress(ImportError):
            import recsa_challenge.appointments.signals  # noqa: F401, PLC0415
