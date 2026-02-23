from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'
    label = 'projects'
    verbose_name = _('Projects & Time Tracking')

    def ready(self):
        pass
