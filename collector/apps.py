from django.apps import AppConfig
from django.apps import AppConfig


class CollectorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collector"


class CollectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collector'

    def ready(self):
        # This import is vital!
        import collector.signals


from django.apps import AppConfig

class CollectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collector'

    def ready(self):
        # This import is critical for the signal to work
        import collector.signals