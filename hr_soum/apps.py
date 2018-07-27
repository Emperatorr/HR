from django.apps import AppConfig


class HRAppConfig(AppConfig):
    name = 'hr_soum'

    def ready(self):
        import signals.signals