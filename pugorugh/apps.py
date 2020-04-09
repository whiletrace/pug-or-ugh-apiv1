from django.apps import AppConfig


class PugorughConfig(AppConfig):
    name = 'pugorugh'

    def ready(self):
        import pugorugh.signals
