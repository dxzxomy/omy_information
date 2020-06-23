from django.apps import AppConfig


class RepoConfig(AppConfig):
    name = 'apps.windowsad'
    verbose_name = "windowsAD"

    def ready(self):
        from .signal import handler