from django.apps import AppConfig


class HRAppConfig(AppConfig):
    name = 'hr_leaves'

    def ready(self):
        import signals.signals